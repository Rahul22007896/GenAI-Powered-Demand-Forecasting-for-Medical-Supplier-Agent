from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import httpx
import json
import os
from typing import List, Dict, Any
import re

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "demand_forecasting",
    "user": "postgres",
    "password": "Rahul@2026"
}

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    data: List[Dict[str, Any]]
    columns: List[str]
    row_count: int

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    with conn.cursor() as cur:
        cur.execute("SET search_path TO raw_data, public;")
    return conn

async def generate_sql_from_query(user_query: str) -> str:

    schema_context = """
Schema: raw_data

Table: raw_data.products
- product_id (SERIAL PRIMARY KEY)
- product_name (VARCHAR)
- category (VARCHAR)
- manufacturer (VARCHAR)
- unit_price (DECIMAL)

Table: raw_data.demand_history
- demand_id (SERIAL PRIMARY KEY)
- product_id (INTEGER, FK to products)
- date (DATE)
- quantity_sold (INTEGER)
- revenue (DECIMAL)
- region (VARCHAR)

Table: raw_data.demand_forecasts
- forecast_id (SERIAL PRIMARY KEY)
- product_id (INTEGER, FK to products)
- forecast_date (DATE)
- predicted_quantity (INTEGER)
- confidence_level (DECIMAL)
"""

    prompt = f"""
Convert the following question into a valid PostgreSQL SELECT query.

Schema:
{schema_context}

Question:
{user_query}

Rules:
- Use schema name raw_data
- Use JOIN between products and demand_history
- Use LEFT JOIN for demand_forecasts (forecast data may be missing)
- Use ILIKE for text search
- Always LIMIT results to 100 rows
- Do NOT assume historical date ranges unless user specifies
- If the query looks like a company or brand name, search manufacturer
- If the query looks like a product name, search product_name
- If unsure, search BOTH product_name and manufacturer using OR
- Return ONLY SQL
- Do NOT add date filters unless the user explicitly asks for a date range.
- Use DISTINCT or GROUP BY when duplicate rows may appear.
- Use DISTINCT or GROUP BY when products have multiple manufacturers.
- Avoid using DISTINCT. Use GROUP BY or DISTINCT ON when needed.
- NEVER use placeholders like your_search_term
- NEVER include SQL comments (-- or /* */)
- Use actual values derived from the user question
- If no filter is specified, DO NOT add a WHERE clause
- Avoid using DISTINCT.
- If DISTINCT is used, include all ORDER BY columns in SELECT.
- Prefer GROUP BY or DISTINCT ON instead.
- Always include profile_page_url when selecting from products.


SQL:
"""

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "Demand Forecasting App"
            },
            json={
                "model": "meta-llama/llama-3.1-8b-instruct",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 512
            }
        )

        if response.status_code != 200:
            print("OpenRouter Status:", response.status_code)
            print("OpenRouter Response:", response.text)
            raise HTTPException(status_code=500, detail="LLM API failed")

        result = response.json()
        sql_query = result["choices"][0]["message"]["content"]

        # ---------------- CLEAN SQL ----------------

        # remove markdown
        sql_query = sql_query.replace("```sql", "").replace("```", "")

        # remove weird tokens like [s<eos>]
        sql_query = re.sub(r"\[.*?\]", "", sql_query)
        
        # remove placeholder tokens
        if "your_search_term" in sql_query.lower():
            raise HTTPException(
        status_code=400,
        detail="Invalid SQL generated. Please refine your query."
    )
        # keep only first statement
        if ";" in sql_query:
            sql_query = sql_query.split(";")[0] + ";"

        sql_query = sql_query.strip()
        
        # ---------------- SAFETY CHECK ----------------
        if not sql_query.lower().startswith("select"):
            raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")
        
        if "your_search_term" in sql_query.lower():
            raise HTTPException(status_code=400, detail="Invalid SQL generated")

        return sql_query
    
async def call_llm(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "Demand Forecasting App"
            },
            json={
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional pharmaceutical demand forecasting analyst."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens":400 
            }
        )

        if response.status_code != 200:
            print("LLM ERROR:", response.text)
            raise HTTPException(status_code=500, detail="LLM generation failed")

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        # 🔹 Normalize user input (VERY IMPORTANT)
        user_query = request.query.strip()

        # If user types only a keyword like "injectables"
        if len(user_query.split()) == 1:
            user_query = f"Show data for {user_query}"
        
        if user_query.lower() in ["show demand history", "demand history"]:
            user_query = "Show all demand history"

        # Generate SQL from normalized query
        sql_query = await generate_sql_from_query(user_query)

        print(f"Generated SQL: {sql_query}")  # Debug log

        # Execute SQL query
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(sql_query)
        results = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description] if cursor.description else []

        cursor.close()
        conn.close()

        data = [dict(row) for row in results]

        return QueryResponse(
            data=data,
            columns=columns,
            row_count=len(data)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/api/product/forecast-insight")
async def generate_forecast_insight():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
          p.product_id,
          p.product_name,
          p.manufacturer,
          SUM(d.quantity_sold) AS total_demand,
          AVG(f.predicted_quantity) AS avg_forecast
        FROM raw_data.products p
        LEFT JOIN raw_data.demand_history d ON p.product_id = d.product_id
        LEFT JOIN raw_data.demand_forecasts f ON p.product_id = f.product_id
        WHERE p.product_name = 'Injectables'
          AND p.manufacturer = 'Sun Pharma'
        GROUP BY p.product_id, p.product_name, p.manufacturer
    """)

    product_row = cur.fetchone()

    if product_row is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # 🔹 Check if insight already exists
    cur.execute("""
        SELECT forecast_insight
        FROM raw_data.products
        WHERE product_id = %s
    """, (product_row["product_id"],))

    existing = cur.fetchone()

    if existing and existing["forecast_insight"]:
        cur.close()
        conn.close()
        return {
            "product": product_row["product_name"],
            "manufacturer": product_row["manufacturer"],
            "insight": existing["forecast_insight"]
        }

    # 🔹 Generate new insight
    prompt = f"""
You are a pharmaceutical demand forecasting expert.

Product: {product_row['product_name']}
Manufacturer: {product_row['manufacturer']}

Total historical demand: {product_row['total_demand']}
Average forecasted demand: {product_row['avg_forecast']}

Generate a professional forecast analysis including:
- demand trend
- supply risk
- inventory recommendation
"""

    insight_text = await call_llm(prompt)

    cur.execute("""
        UPDATE raw_data.products
        SET forecast_insight = %s
        WHERE product_id = %s
    """, (insight_text, product_row["product_id"]))

    conn.commit()
    cur.close()
    conn.close()

    return {
        "product": product_row["product_name"],
        "manufacturer": product_row["manufacturer"],
        "insight": insight_text
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
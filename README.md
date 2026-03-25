# GenAI Powered Demand Forecasting for Medical Supplier Agent

##  Overview

PharmaCast is an AI-powered demand forecasting analytics platform that enables users to query pharmaceutical and medical supply data using natural language.

It leverages Large Language Models (LLMs) to:

* Convert user queries → SQL
* Retrieve structured data from PostgreSQL
* Generate intelligent forecasting insights

This transforms traditional dashboards into **conversational AI-driven analytics systems** 

---

## Goal

Build a full-stack AI system that:

* Accepts natural language queries
* Converts them into safe SQL queries
* Fetches demand data from a database
* Generates AI-powered forecasting insights

---

## Key Features

### Natural Language Query Engine

Users can ask:

* “Show demand history for Injectables”
* “Get sales data for Sun Pharma products”

LLM converts query → safe PostgreSQL `SELECT` query

---

### Data Analytics Engine

* Executes SQL queries on PostgreSQL
* Returns structured JSON results
* Preserves column metadata for UI

---

### Forecast Insight Generation

* Aggregates demand + forecast data
* Uses LLM to generate:

  * Demand trends
  * Supply risks
  * Inventory recommendations
* Stores insights in database

---

##  System Architecture

```id="arch01"
User Query (Natural Language)
        ↓
LLM (NL → SQL)
        ↓
FastAPI Backend
        ↓
PostgreSQL Database
        ↓
LLM (Insight Generation)
        ↓
Frontend Dashboard (React)
```

---

##  Tech Stack

### Backend

* Python
* FastAPI
* PostgreSQL
* Psycopg2
* httpx (LLM API calls)

### Frontend

* React (Vite)

### AI / LLM

* LLM Model Through API KEY

### Database

* PostgreSQL (raw_data schema)

---


##  Backend Workflow

### 1. Natural Language → SQL

* User submits query
* LLM generates SQL
* Only safe, read-only queries allowed

---

### 2️. SQL Execution

* Query executed in PostgreSQL
* Results returned as JSON

---

### 3️. Forecast Insight Generation

* Aggregate demand history
* Compute forecast averages
* Generate AI insight via LLM
* Store insights in database

---

## Frontend Workflow

### Dashboard Page

* Search input
* Query button
* Results table with:

  * Product
  * Manufacturer
  * Revenue
  * Forecast

---

### Forecast Page

Route:

```id="route01"
/forecast/:product/:manufacturer
```

Displays:

* Product details
* Demand summary
* AI-generated insights
* Recommendations

---

## Future Enhancements

* Real-time forecasting
* Cloud deployment (AWS)
* Advanced dashboards
* Multi-model LLM support

---

## Conclusion

This project demonstrates how LLMs can transform traditional analytics systems into intelligent, conversational platforms.

PharmaCast bridges the gap between **raw data and decision-making insights** 

---

## Support

If you like this project, give it a ⭐ on GitHub!

# GenAI-Powered Demand Intelligence Agent – System Design

## 1. Architecture Overview
The system follows a **GenAI-powered NL → SQL → Insight architecture**. It does not rely on ML or statistical forecasting models. Instead, it combines LLM-based intent understanding and SQL generation with deterministic database queries, rule-based logic, and GenAI-generated explanations.

**High-level flow:**  
User Query → LLM Intent & SQL Generation → PostgreSQL Execution → Rule-Based Signal Processing → Risk Labeling → GenAI Explanation → UI Response

This architecture prioritizes **explainability, auditability, and operational safety**, which are critical in healthcare supply chains.

## 2. Core Components

### 2.1 Web & API Layer
- Web UI for natural language queries
- FastAPI backend exposing query and insight endpoints
- CORS-enabled secure communication

### 2.2 LLM-Based Query Understanding
- Uses an LLM to interpret user intent
- Converts free-text queries into valid PostgreSQL SELECT statements
- Enforces schema awareness and strict SQL generation rules

### 2.3 SQL Safety & Validation Layer
- Ensures only SELECT queries are executed
- Removes unsafe tokens, placeholders, and comments
- Limits result size and enforces grouping rules

### 2.4 Data Layer (PostgreSQL)
- Product master data
- Historical demand records
- Optional forecast reference tables
- Cached insight storage

### 2.5 Rule-Based Signal Processing
- Aggregates historical demand using SQL results
- Applies deterministic business rules
- Adjusts interpretation using external signals such as:
  - Seasonality calendars
  - Disease outbreak indicators

### 2.6 Risk Labeling Module
- Assigns LOW / MEDIUM / HIGH risk labels
- Based on deviation thresholds, trend deltas, and external signals
- Fully deterministic and explainable

### 2.7 GenAI Insight Generation
- Converts numeric outputs into professional analytical narratives
- Explains demand trends, risks, and inventory considerations
- Guardrailed prompts prevent hallucination or unsupported claims

## 3. Data Flow
1. User submits a natural language query
2. LLM generates a safe SQL query
3. PostgreSQL executes the query and returns results
4. Rule engine evaluates trends and external signals
5. Risk label is assigned
6. GenAI generates an explanatory insight
7. Response is returned to the frontend

## 4. Technology Stack
- Backend: Python, FastAPI
- Database: PostgreSQL
- GenAI: OpenRouter / OpenAI-compatible LLMs
- Frontend: React
- External Data: Public health alerts, seasonality datasets

## 5. Security & Responsible AI Design
- Role-based database access
- SQL injection prevention via validation
- SELECT-only enforcement
- Transparent, explainable outputs
- No black-box predictive models

## 6. Scalability & Reliability
- Stateless API design
- Horizontal scaling for API and LLM calls
- Cached insights reduce repeated computation

## 7. Design Trade-offs
- Explainability over predictive sophistication
- Deterministic rules over adaptive ML models
- Transparency prioritized for healthcare use cases

## 8. Failure Modes & Mitigations
- LLM SQL errors → strict validation and rejection
- Missing external signals → fallback to historical data only
- Inconsistent data → database-level constraints

## 9. Future Extensions
- User-configurable business rules
- Multi-region demand comparison
- Integration with inventory management systems


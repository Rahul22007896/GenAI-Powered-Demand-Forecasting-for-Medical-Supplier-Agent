CREATE SCHEMA IF NOT EXISTS raw_data;

SET search_path TO raw_data, public;

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    manufacturer VARCHAR(255),
    unit_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS demand_history (
    demand_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    date DATE NOT NULL,
    quantity_sold INTEGER,
    revenue DECIMAL(10, 2),
    region VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS demand_forecasts (
    forecast_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    forecast_date DATE NOT NULL,
    predicted_quantity INTEGER,
    confidence_level DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products (product_name, category, manufacturer, unit_price)
VALUES ('Dolo 650', 'Pharmaceutical', 'Micro Labs', 3.50);

INSERT INTO demand_history (product_id, date, quantity_sold, revenue, region)
VALUES 
    (1, '2024-01-01', 1500, 5250.00, 'North'),
    (1, '2024-01-02', 1800, 6300.00, 'North'),
    (1, '2024-01-03', 1200, 4200.00, 'South');

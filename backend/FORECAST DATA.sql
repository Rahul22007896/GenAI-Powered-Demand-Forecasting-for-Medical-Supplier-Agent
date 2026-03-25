SET search_path TO raw_data, public;

INSERT INTO raw_data.demand_forecasts
(product_id, forecast_date, predicted_quantity, confidence_level)
SELECT
  product_id,
  DATE '2024-02-15',
  FLOOR(random() * 600 + 200)::INT,
  ROUND((random() * 0.2 + 0.75)::NUMERIC, 2)
FROM raw_data.products;

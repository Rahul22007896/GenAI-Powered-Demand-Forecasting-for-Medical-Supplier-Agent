SET search_path TO raw_data, public;

INSERT INTO demand_history
(product_id, date, quantity_sold, revenue, region)
SELECT
  product_id,
  DATE '2024-01-15',        -- date column
  qty,                      -- quantity_sold
  qty * unit_price,         -- revenue
  'South'                   -- region
FROM (
  SELECT
    product_id,
    FLOOR(random() * 100 + 20)::INT AS qty,
    unit_price
  FROM products
) t;

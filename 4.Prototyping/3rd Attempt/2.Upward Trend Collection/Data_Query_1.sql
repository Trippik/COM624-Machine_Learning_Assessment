SELECT
DATEDIFF(product_values.record_date, (SELECT MIN(record_date) FROM product_values)) AS date_rate,
product_values.record_date,
product_values.open_value 
FROM product_values
WHERE product_values.product = 3
ORDER BY product_values.record_date 
LIMIT 300
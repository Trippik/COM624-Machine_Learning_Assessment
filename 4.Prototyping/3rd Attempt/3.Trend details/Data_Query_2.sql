SELECT
product_values.product,
product_values.record_date,
product_values.open_value 
FROM product_values
WHERE product_values.record_date > "2020-01-01"
ORDER BY product, product_values.record_date 
LIMIT 10000
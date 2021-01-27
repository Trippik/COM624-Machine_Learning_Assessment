SELECT
product_values.id,
product.product_name,
product_values.record_date,
product.product_type,
currency.currency_name,    
ROUND((product_values.close_value - product_values.open_value), 2) AS "Daily Return",
ROUND((product_values.high_value - product_values.low_value), 2) AS "Daily Range",
ROUND((((product_values.close_value - product_values.open_value) / product_values.open_value) * 100),2) AS "Percentage Daily Return",
(SELECT MIN(record_date) FROM product_values WHERE product_values.product = product.id) AS EarliestRecord,
(SELECT MAX(record_date) FROM product_values WHERE product_values.product = product.id) AS LatestRecord
FROM product_values
LEFT JOIN product ON product_values.product = product.id
LEFT JOIN currency ON product.currency = currency.id
WHERE
(product.id = 3)
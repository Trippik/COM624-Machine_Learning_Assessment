SELECT
product_values.id,
product.product_name,      
product.product_type,      
product_values.open_value, 
product_values.close_value,
product_values.high_value, 
product_values.low_value,  
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
(product.id = 20362 OR 8526 OR 5561 OR 31549 OR 19772 OR 35616 OR 34106 OR 42526 OR 12377 OR 32494 OR 14874 OR 44036 OR 41598 OR 46269 OR 11169 OR 18084 OR 19435 OR 44412 OR 41704 OR 22341)
AND (SELECT MAX(record_date) FROM product_values WHERE product_values.product = product.id) = "2020-11-27"
SELECT
product_values.id,
DATEDIFF(product_values.record_date, (SELECT MIN(product_values.record_date) FROM product_values WHERE product_values.product = 3)) AS date_rate,
(SELECT ROUND((product_values.close_value - product_values.open_value), 2) FROM product_values WHERE product = 3 AND record_date = date_rate - 3)
ROUND((product_values.close_value - product_values.open_value), 2) AS "Daily Return",
ROUND((product_values.high_value - product_values.low_value), 2) AS "Daily Range",
ROUND((((product_values.close_value - product_values.open_value) / product_values.open_value) * 100),2) AS "Percentage Daily Return"
FROM product_values
LEFT JOIN product ON product_values.product = product.id
LEFT JOIN currency ON product.currency = currency.id
WHERE
(product.id = 3)
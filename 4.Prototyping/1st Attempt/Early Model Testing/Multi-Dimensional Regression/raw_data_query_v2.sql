SELECT
DATEDIFF(product_values.record_date, (SELECT MIN(product_values.record_date) FROM product_values WHERE product_values.product = 3)) AS date_rate,
product.product_type,
currency.id, 
product_values.close_value,
product_values.high_value,
product_values.low_value,
product_values.open_value,
product_values.volume,
product_values.adj_close,
product_values.adj_low,
product_values.adj_volume,
product_values.div_cash,
product_values.split_factor,
ROUND((product_values.close_value - product_values.open_value), 2) AS "daily_return",
ROUND((product_values.close_value - product_values.open_value), 2) AS "daily_range",
ROUND((((product_values.close_value - product_values.open_value) / product_values.open_value) * 100),2) AS "percentage_daily_return"
FROM product_values
LEFT JOIN product ON product_values.product = product.id
LEFT JOIN currency ON product.currency = currency.id
WHERE
(product.id = 3)
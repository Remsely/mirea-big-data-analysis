SELECT date_trunc('month', order_purchase_timestamp) AS time,
       COUNT(order_id)                               AS value,
       'Orders Count'                                AS metric
FROM orders
GROUP BY 1
ORDER BY 1;

SELECT customer_state                                                                              AS metric,
       ROUND(AVG(EXTRACT(DAY FROM (order_delivered_customer_date - order_purchase_timestamp))), 1) as value
FROM orders o
         JOIN customers c ON o.customer_id = c.customer_id
WHERE order_delivered_customer_date IS NOT NULL
GROUP BY customer_state
ORDER BY value DESC;

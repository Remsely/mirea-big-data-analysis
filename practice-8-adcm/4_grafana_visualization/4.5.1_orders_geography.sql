SELECT customer_state     AS metric,
       COUNT(customer_id) AS value
FROM customers
GROUP BY customer_state
ORDER BY value DESC;

SELECT payment_type             AS metric,
       COUNT(distinct order_id) AS value
FROM order_payments
GROUP BY payment_type;

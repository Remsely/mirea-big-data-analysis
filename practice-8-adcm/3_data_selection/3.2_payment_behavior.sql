WITH total_unique_orders AS (SELECT COUNT(DISTINCT order_id) as total_cnt
                             FROM order_payments)
SELECT payment_type,
       COUNT(*)                            AS payments_count,
       ROUND(AVG(payment_installments), 2) AS avg_installments,
       ROUND(AVG(payment_value), 2)        AS avg_payment_value,
       ROUND(
               (COUNT(DISTINCT order_id)::numeric / (SELECT total_cnt FROM total_unique_orders)) * 100,
               2
       )                                   AS order_share_percent
FROM order_payments
GROUP BY payment_type
ORDER BY payments_count DESC;

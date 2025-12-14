SELECT s.seller_id,
       COUNT(DISTINCT oi.order_id)          AS unique_orders,
       COUNT(DISTINCT c.customer_unique_id) AS unique_customers,
       COUNT(oi.product_id)                 AS items_sold,
       SUM(oi.price)                        AS total_revenue,
       ROUND(AVG(oi.freight_value), 2)      AS avg_freight_cost
FROM sellers s
         JOIN order_items oi ON s.seller_id = oi.seller_id
         JOIN orders o ON oi.order_id = o.order_id
         JOIN customers c ON o.customer_id = c.customer_id
GROUP BY s.seller_id
ORDER BY unique_orders DESC
LIMIT 10;

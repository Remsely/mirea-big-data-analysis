SELECT t.product_category_name_english AS category_name_en,
       SUM(oi.price)                   AS revenue,
       COUNT(DISTINCT oi.order_id)     AS unique_orders_count,
       COUNT(oi.product_id)            AS total_items_count
FROM order_items oi
         JOIN products p ON oi.product_id = p.product_id
         JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
GROUP BY t.product_category_name_english
ORDER BY revenue DESC
LIMIT 10;

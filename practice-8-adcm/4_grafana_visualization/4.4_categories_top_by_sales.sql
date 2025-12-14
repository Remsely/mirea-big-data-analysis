SELECT t.product_category_name_english AS metric,
       SUM(oi.price)                   AS value
FROM order_items oi
         JOIN products p ON oi.product_id = p.product_id
         JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
GROUP BY t.product_category_name_english
ORDER BY value DESC
LIMIT 10;

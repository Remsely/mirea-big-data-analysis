WITH delivery_data AS (SELECT o.order_id,
                              CASE
                                  WHEN EXTRACT(DAY FROM
                                               (o.order_delivered_customer_date - o.order_purchase_timestamp)) <= 5
                                      THEN '0-5 days'
                                  WHEN EXTRACT(DAY FROM
                                               (o.order_delivered_customer_date - o.order_purchase_timestamp)) BETWEEN 6 AND 10
                                      THEN '6-10 days'
                                  ELSE '> 10 days'
                                  END AS delivery_interval
                       FROM orders o
                       WHERE o.order_delivered_customer_date IS NOT NULL
                         AND o.order_purchase_timestamp IS NOT NULL)
SELECT dd.delivery_interval,
       COUNT(DISTINCT dd.order_id)   AS orders_count,
       ROUND(AVG(r.review_score), 2) AS avg_review_score
FROM delivery_data dd
         JOIN order_reviews r ON dd.order_id = r.order_id
GROUP BY dd.delivery_interval
ORDER BY CASE dd.delivery_interval
             WHEN '0-5 days' THEN 1
             WHEN '6-10 days' THEN 2
             ELSE 3
             END;

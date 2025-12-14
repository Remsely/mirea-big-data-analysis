SELECT CAST(review_score AS TEXT) AS metric,
       COUNT(distinct order_id)   AS value
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;

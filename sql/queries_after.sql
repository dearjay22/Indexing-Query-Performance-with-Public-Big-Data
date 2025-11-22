-- After indexes queries (same as baseline)
USE bigdata;

SELECT borough, COUNT(*) AS cnt
FROM nyc311
WHERE created_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY borough
ORDER BY cnt DESC;

SELECT complaint_type, AVG(TIMESTAMPDIFF(HOUR, created_date, closed_date)) AS avg_hours
FROM nyc311
WHERE closed_date IS NOT NULL
GROUP BY complaint_type
ORDER BY avg_hours DESC
LIMIT 20;

SELECT complaint_type, COUNT(*) AS cnt
FROM nyc311
WHERE incident_zip IN ('10007','10006','10005')
GROUP BY complaint_type
ORDER BY cnt DESC
LIMIT 20;

-- FULLTEXT queries using correct column
SELECT unique_key, created_date, descriptor
FROM nyc311
WHERE descriptor LIKE '%noise%'
LIMIT 100;

SELECT COUNT(*) AS cnt_rodent_like 
FROM nyc311 
WHERE descriptor LIKE '%rodent%';

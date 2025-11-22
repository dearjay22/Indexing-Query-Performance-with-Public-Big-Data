USE bigdata;

-- Example: check query plan for complaints by borough
EXPLAIN FORMAT=JSON
SELECT borough, COUNT(*) as total
FROM nyc311
GROUP BY borough;

-- Example: check query plan for complaints by complaint_type
EXPLAIN FORMAT=JSON
SELECT complaint_type, COUNT(*) as total
FROM nyc311
GROUP BY complaint_type;

-- Example: check query plan for complaints in a certain ZIP code
EXPLAIN FORMAT=JSON
SELECT *
FROM nyc311
WHERE incident_zip = '10001';

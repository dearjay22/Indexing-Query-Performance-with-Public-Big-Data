
USE bigdata;
SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE '/workspaces/Indexing-Query-Performance-with-Public-Big-Data/data/dataset.csv'
INTO TABLE nyc311
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(unique_key, created_date, closed_date, agency, agency_name, complaint_type, descriptor, location_type, incident_zip, city, borough, latitude, longitude, status, resolution_description);

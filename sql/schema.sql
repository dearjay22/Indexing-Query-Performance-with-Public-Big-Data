CREATE DATABASE IF NOT EXISTS bigdata;

USE bigdata;

CREATE TABLE IF NOT EXISTS nyc311 (
    unique_key BIGINT PRIMARY KEY,
    created_date DATETIME,
    closed_date DATETIME,
    agency VARCHAR(100),
    agency_name VARCHAR(100),
    complaint_type VARCHAR(255),
    descriptor VARCHAR(255),
    location_type VARCHAR(100),
    incident_zip VARCHAR(10),
    city VARCHAR(100),
    borough VARCHAR(100),
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    status VARCHAR(50),
    resolution_description TEXT
);

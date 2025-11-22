USE bigdata;

-- B-tree indexes
CREATE INDEX idx_created_date ON nyc311(created_date);
CREATE INDEX idx_created_borough ON nyc311(created_date, borough);
CREATE INDEX idx_complaint_type ON nyc311(complaint_type(100));
CREATE INDEX idx_borough ON nyc311(borough);

-- FULLTEXT index
ALTER TABLE nyc311 ADD FULLTEXT ft_complaint_summary (complaint_summary);

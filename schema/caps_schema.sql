-- for local dev setup uncomment the lines below and run in psql as the admin user
-- CREATE ROLE caps;
-- ALTER ROLE caps LOGIN;
-- ALTER ROLE caps WITH PASSWORD ''; -- provide a password
-- CREATE SCHEMA IF NOT EXISTS caps;
-- GRANT USAGE ON SCHEMA caps TO caps;
DROP TABLE IF EXISTS caps.client_calls CASCADE;
CREATE TABLE IF NOT EXISTS caps.client_calls (
    request_id SERIAL PRIMARY KEY,
    received_timestamp TIMESTAMP,
    ip_address VARCHAR(20),
    response_code INTEGER,
    raw_data VARCHAR(4095),
    environment VARCHAR(50),
    namespace VARCHAR(255),
    app_id VARCHAR(255),
    device_created_timestamp TIMESTAMP,
    event_data_json VARCHAR(4095)
);
ALTER TABLE caps.client_calls OWNER TO caps; 
DROP TABLE IF EXISTS caps.snowplow_calls;
CREATE TABLE IF NOT EXISTS caps.snowplow_calls (
    snowplow_send_id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES caps.client_calls(request_id),
    sent_timestamp TIMESTAMP,
    snowplow_response INTEGER,
    try_number INTEGER,
    environment VARCHAR(50),
    namespace VARCHAR(255),
    app_id VARCHAR(255),
    device_created_timestamp TIMESTAMP,
    event_data_json VARCHAR(4095)
);
ALTER TABLE caps.snowplow_calls OWNER TO caps;

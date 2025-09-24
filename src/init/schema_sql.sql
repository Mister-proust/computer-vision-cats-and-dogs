CREATE SCHEMA IF NOT EXISTS monitoring;

CREATE TABLE IF NOT EXISTS monitoring.time_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    inference_time_ms FLOAT NOT NULL,
    success BOOLEAN NOT NULL
);


CREATE TABLE IF NOT EXISTS monitoring.feedbackusers (
    id SERIAL PRIMARY KEY, 
    image_data BYTEA NOT NULL,               
    feedback BOOLEAN,                         
    prediction VARCHAR(50) NOT NULL,         
    time_metric_id INTEGER,                   
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (time_metric_id) REFERENCES monitoring.time_metrics(id)
        ON DELETE SET NULL                    -
);
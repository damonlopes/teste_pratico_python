CREATE TABLE IF NOT EXISTS flights (
    id SERIAL PRIMARY KEY,
    flight_date TIMESTAMP NOT NULL,
    flight_iata TEXT,
    flight_status TEXT,
    airline TEXT NOT NULL,
    dep_iata TEXT NOT NULL,
    dep_delay INTEGER,
    arr_iata TEXT NOT NULL,
    arr_delay INTEGER
)
DROP TABLE IF EXISTS potholes;

CREATE TABLE potholes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    street_addr TEXT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    size INTEGER NOT NULL,
    location TEXT NOT NULL,
    other TEXT,
    repair_status TEXT NOT NULL,
    repair_type TEXT NOT NULL,
    repair_priority TEXT NOT NULL,
    report_date TEXT NOT NULL,
    expected_completion TEXT NOT NULL
);
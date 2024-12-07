DROP TABLE IF EXISTS Potholes;
DROP TABLE IF EXISTS WorkOrders;

CREATE TABLE Potholes (
    pothole_id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    street_addr TEXT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    size INTEGER NOT NULL,
    location TEXT NOT NULL,
    other_info TEXT,
    repair_status TEXT NOT NULL,
    repair_type TEXT NOT NULL,
    repair_priority TEXT NOT NULL,
    report_date TEXT NOT NULL,
    expected_completion TEXT NOT NULL,
    actual_completion TEXT
);

CREATE TABLE WorkOrders (
    work_order_id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    pothole_id INTEGER NOT NULL UNIQUE,
    assignment_date TEXT NOT NULL,
    estimated_man_hours INTEGER NOT NULL,
    actual_man_hours INTEGER,
    FOREIGN KEY (pothole_id) REFERENCES Potholes (pothole_id)
);
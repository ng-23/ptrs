DROP TABLE IF EXISTS potholes;

CREATE TABLE potholes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    street_addr TEXT NOT NULL,
    size INTEGER NOT NULL,
    location TEXT NOT NULL,
    repair_type TEXT NOT NULL,
    repair_priority TEXT NOT NULL
);

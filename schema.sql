DROP TABLE IF EXISTS company;

CREATE TABLE company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    industry TEXT NOT NULL,
    summary TEXT NOT NULL
);

DROP TABLE IF EXISTS consumptions;

CREATE TABLE consumptions (
    company_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    electricity TEXT NOT NULL,
    water TEXT NOT NULL,
    co2 TEXT NOT NULL,
    PRIMARY KEY (company_id, year, month)
);

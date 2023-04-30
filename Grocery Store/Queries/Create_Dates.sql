CREATE TABLE IF NOT EXISTS Dates(
    DateId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Date TEXT,
    Year INTEGER,
    Month INTEGER,
    Day INTEGER
);

CREATE TEMP TABLE Temp_Dates AS
SELECT DISTINCT Date
FROM Grocery_Store.Purchases;

SELECT *
FROM temp.Temp_Dates;

INSERT INTO Dates(Date, Day, Month, Year)
SELECT DISTINCT Date, CAST(SUBSTR(Date, 9,2) AS INTEGER) AS Day, CAST(SUBSTR(Date, 6,2) AS INTEGER) AS Month, CAST(SUBSTR(Date, 1) AS INTEGER) AS Year
FROM Grocery_Store.Purchases
ORDER BY Date ASC;

SELECT *
FROM Dates;

DROP TABLE temp.Temp_Dates;


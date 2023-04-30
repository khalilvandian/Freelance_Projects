SELECT Member_Number, Count(Member_Number) as TCount
FROM Purchases
GROUP BY Member_Number
ORDER BY Member_Number;

SELECT DISTINCT Item
FROM Purchases;

SELECT DISTINCT Member_Number, LENGTH(Member_Number) AS Len
FROM Purchases
ORDER BY Len;

SELECT DISTINCT Date, SUBSTR(Date, 7) || "-" || SUBSTR(Date, 4, 2) || "-" || SUBSTR(Date, 1, 2) AS NewDate
FROM Purchases
ORDER BY NewDate;

ALTER TABLE Purchases
ADD Year INTEGER;

SELECT Date, CAST(SUBSTR(Date, 7) AS Text) AS Year
FROM Purchases
ORDER BY Year;

INSERT INTO Purchases (Year)
SELECT CAST(SUBSTR(Date, 7) AS INTEGER) AS Year
FROM Purchases;

ALTER TABLE Purchases
ADD Month INTEGER;

ALTER TABLE Purchases
ADD Day INTEGER;

SELECT *, CAST(SUBSTR(Date, 1,2) AS INTEGER) AS Day, CAST(SUBSTR(Date, 4,2) AS INTEGER) AS Month, CAST(SUBSTR(Date, 7) AS INTEGER) AS Year
FROM Purchases

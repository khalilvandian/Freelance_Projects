CREATE TEMP TABLE Pur_Temp AS
SELECT Member_number as MemberId, TRIM(Date) AS Date, TRIM(itemDescription) AS Item
FROM Purchases_Unclean;

CREATE TABLE Purchases AS
SELECT MemberId, Item,
        SUBSTR(Date, 7) || "-" || SUBSTR(Date, 4,2) || "-" || SUBSTR(Date, 1,2) AS Date
FROM temp.Pur_Temp;

DROP TABLE temp.Pur_Temp;

SELECT *
FROM Purchases
ORDER BY Item



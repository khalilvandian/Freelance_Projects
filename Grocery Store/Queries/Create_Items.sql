CREATE TABLE IF NOT EXISTS Items(
    ItemId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Name TEXT NOT NULL
);

CREATE TEMP TABLE Temp_Items AS
SELECT DISTINCT Item
FROM Grocery_Store.Purchases;


SELECT *
FROM temp.Temp_Items;

INSERT INTO Items(Name)
SELECT Item
FROM temp.Temp_Items;

SELECT *
FROM Items;

DROP TABLE temp.Temp_Items;
SELECT MemberId, MAX(Date) AS Last_Purchase_Date, COUNT(DISTINCT Date) AS Frequency, COUNT() AS MonetaryValue
FROM Purchases
GROUP BY MemberId
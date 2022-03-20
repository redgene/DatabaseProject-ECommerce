-- multirelation

-- A Customer (with CustomerID TG-9442789) wants to check which products are there in the cart.
SELECT ProductID from ProductsInCart
WHERE CartID 
IN (SELECT CartID FROM Cart WHERE CustomerID = 'TG-9442789');

-- A Seller wishes to thank all the customers that have purchased from them + get some feedback
--	For that, they need their names and email IDs.
SELECT CustomerFirstName, CustomerLastName, CustomerEmail FROM Customer
WHERE CustomerID in (SELECT CustomerID FROM Orders WHERE SellerID = 'MPKR-2298');

-- The company is interested in expanding the businesses by 
--	adding more sellers to states where the people tend not 
--	to buy (have products that amount to a maximum).
SELECT CartTotal, CustomerAddressState FROM Cart 
NATURAL JOIN Customer order by CartTotal desc;

-- The company is interested in knowing all the postal companies that 
-- 	are co-located with Sellers, so that it can match them up if required.
SELECT PostalCompanyName, SellerID FROM PostalCompany 
INNER JOIN Seller 
ON PostalCompany.PostalCompanyHQ = Seller.SellerAddressCity;

-- The company is looking to acquire sellers that have a strong foothold in their respective states
--	and therefore is interested in knowing the maximum possible availabilities wrt their inventories
select SellerID, SUM(Inventory) AS Total_Availability, SellerAddressState 
FROM SellerProductMapping natural join Seller group by SellerID order by Total_Availability desc;
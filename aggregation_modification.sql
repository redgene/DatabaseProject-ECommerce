-- AGGREGATION QUERIES
-- Interested in knowing the average price per category, but want category name (which is in a different table)
select CategoryName, AVG(PriceNew) from Product natural join Category group by CategoryID;

-- Some products are returned more often, leading to them being resold again. The ECom company is interested in knowing
--	the average price differences and average customer reviews and hope to relate them later
select Brand, CustomerAverageReview, (PriceNew-PriceUsed) as Difference from Product order by Difference desc;

-- Interested in knowing the average of customer reviews for all products for different Countries
select CountryOrigin, AVG(CustomerAverageReview) from Product group by CountryOrigin;


-- COUNT TUPLES IN EACH TABLE
select count(*) as Number_of_Tuples_in_Customer from (Customer);
select count(*) as Number_of_Tuples_in_Product from (Product);
select count(*) as Number_of_Tuples_in_Seller from (Seller);
select count(*) as Number_of_Tuples_in_Categories from (Category);
select count(*) as Number_of_Tuples_in_PostalCompany from (PostalCompany);
select count(*) as Number_of_Tuples_in_PostalCompanyServingLocations from (PostalCompanyServingLocations);
select count(*) as Number_of_Tuples_in_Orders from (Orders);
select count(*) as Number_of_Tuples_in_Cart from (Cart);
select count(*) as Number_of_Tuples_in_ProductsInCart from (ProductsInCart);
select count(*) as Number_of_Tuples_in_SellerProductMapping from (SellerProductMapping);
select count(*) as Number_of_Tuples_in_SellerPostalCompanyMapping from (SellerPostalCompanyMapping);
select count(*) as Number_of_Tuples_in_ProductRelatedItems from (ProductRelatedItems);


-- MODIFICATION QUERIES
-- Insert a new product tuple
INSERT INTO Product VALUES ('LL-27593413', 'Bello', '#35e847', 'Netherlands', 32, 4.5, 12.3, 11.0, 'GAO');

-- Delete a product
DELETE FROM Product WHERE ProductID = 'LL-27593413';

-- Update a product tuple
UPDATE Product
SET Brand = 'Rhombus'
WHERE ProductID = 'JW-22496313';


-- Insert into Seller & PostalCompany
-- Then use the data from the newly added tuples to add to the SellerPostalCompanyMapping table (6)

INSERT INTO Seller VALUES 
	('FSDX-2235', 'andha.phoda@protonmail.net', '1-467-761-0221', '115-7624 Harper St.', 'New York', 'New York', 295211);
INSERT INTO PostalCompany VALUES 
	(21432, 'FastCourier Ltd', 'Princeton');

INSERT INTO SellerPostalCompanyMapping
SELECT Seller.SellerID, PostalCompany.PostalCompanyID
FROM Seller, PostalCompany
WHERE Seller.SellerEmail = 'andha.phoda@protonmail.net'
AND PostalCompany.PostalCompanyName = 'FastCourier Ltd';


-- Category Percent Share for Gourmet food increased to 23.7% and Collectibles & Fine Art decreased to 1.2%
UPDATE Category SET CategoryPercentShare = 23.7 WHERE CategoryName like '%Gourmet%';
UPDATE Category SET CategoryPercentShare = 1.2  WHERE CategoryName like '%Collectibles%';

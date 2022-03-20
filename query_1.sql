-- A seller using the platform is looking for postal companies that serve in the Chicago area
select PostalCompanyID from PostalCompanyServingLocations where PostalCompanyLocation = 'Chicago';

-- The ecommerce company wants to check the maximum share in profits for different categories, sorted
	-- from max to minimum
select CategoryName, CategoryPercentShare from Category ORDER BY CategoryPercentShare desc;

-- A B2B customer needs to check all sellers for a product that they are interested in
select SellerID, Inventory from SellerProductMapping where ProductID = 'DIBG-5632' AND Inventory <> 0;

-- The ecommerce company wants to tie up with a leading credit card company and needs to show 
	--  proofs that on an average, customers tend to place higher orders on credit cards
	--   as compared to debit cards / online banking
select PaymentMethod, AVG(PriceTotal) from Orders group by PaymentMethod;

-- While browsing the website, a customer finds a specific product that (s)he was looking for, 
	-- but is also interested in alternatives for this. And also compare the prices 
	-- for all the related products
select ProductID, Brand, CountryOrigin, 
	   CustomerReviewsNumber, CustomerAverageReview,
	   PriceNew, PriceUsed, CategoryID from Product where ProductID in
	   (select ProductID2 from ProductRelatedItems where ProductID1 = 'ID-97743186');
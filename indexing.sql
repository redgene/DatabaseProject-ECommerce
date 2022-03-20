.timer on
.eq on
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------

-- BEFORE INDEXES
	-- Run Time: real 0.238 user 0.176735 sys 0.045224

-- AFTER INDEXES
	-- Run Time: real 0.140 user 0.136041 sys 0.001214

-- REASONING:
	-- Process of searching in the Orders containing 100,000 tuples while joining speeds up when indexing is done
	-- The same idea follows while joining Cart with 15,000 tuples.

-- CONFIRMATION:
	-- QUERY PLAN
	-- |--CO-ROUTINE SUBQUERY 3
	-- |  |--MATERIALIZE SUBQUERY 1
	-- |  |  |--SCAN Orders USING INDEX CustomerID_Order_index                          <-----------
	-- |  |  `--SEARCH Customer USING INDEX sqlite_autoindex_Customer_1 (CustomerID=?)
	-- |  |--SCAN SUBQUERY 1
	-- |  `--SEARCH Cart USING INDEX CustomerID_Cart_index (CustomerID=?)               <-----------
	-- `--SCAN SUBQUERY 3

select ((n*sigmaXY)-(sigmaX*sigmaY))/(SQRT ( (n*sigmaX2 - sigmaX_w_2)*(n*sigmaY2 - sigmaY_w_2)  ) ) 
	as correlation 
	from (select  count(*) as n, 
	SUM(x) as sigmaX, SUM(x)*SUM(x) as sigmaX_w_2, SUM(x*x) as sigmaX2,
	SUM(y) as sigmaY, SUM(y)*SUM(y) as sigmaY_w_2, SUM(y*y) as sigmaY2,
	SUM(x*y) as sigmaXY

	from 
	(select CartTotal as x, CartProductsNumber, CustomerID, TotalPurchased as y, 
		CustomerFirstName, CustomerEmail from
		Cart natural join
			(select sum(PriceTotal) as TotalPurchased, CustomerID, CustomerFirstName, CustomerEmail
			from Orders natural join Customer
			group by CustomerID  )

	));

--------------------------------------------------------------------------------------------------------
-- CREATE INDEXES
CREATE INDEX CustomerID_Cart_index     ON Cart (CustomerID);    
CREATE INDEX CustomerID_Order_index    ON Orders (CustomerID);  
--------------------------------------------------------------------------------------------------------


select ((n*sigmaXY)-(sigmaX*sigmaY))/(SQRT ( (n*sigmaX2 - sigmaX_w_2)*(n*sigmaY2 - sigmaY_w_2)  ) ) 
	as correlation 
	from (select  count(*) as n, 
	SUM(x) as sigmaX, SUM(x)*SUM(x) as sigmaX_w_2, SUM(x*x) as sigmaX2,
	SUM(y) as sigmaY, SUM(y)*SUM(y) as sigmaY_w_2, SUM(y*y) as sigmaY2,
	SUM(x*y) as sigmaXY

	from 
	(select CartTotal as x, CartProductsNumber, CustomerID, TotalPurchased as y, 
		CustomerFirstName, CustomerEmail from
		Cart natural join
			(select sum(PriceTotal) as TotalPurchased, CustomerID, CustomerFirstName, CustomerEmail
			from Orders natural join Customer
			group by CustomerID  )

	));


--------------------------------------------------------------------------------------------------------
-- DROP INDEXES
DROP INDEX CustomerID_Cart_index;
DROP INDEX CustomerID_Order_index;

--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------

-- BEFORE INDEXES
	-- Run Time: real 0.015 user 0.015012 sys 0.000357

-- AFTER INDEXES
	-- Run Time: real 0.001 user 0.000952 sys 0.000045

-- REASONING:
	-- Searching in a table of 55000 tuples speeds up if indexingg is done on 2 used columns in Product
	-- There are 15000 tuples which map the relation between reated products in SellerProductMapping
	--  Therefore, searching for right products in the SellerProductMapping is faster after indexing

-- CONFIRMATION:
	-- QUERY PLAN
	-- |--SEARCH Product USING INDEX CountryOrigin_Product_INDEX (CountryOrigin=? AND CustomerAverageReview>?)                
	-- `--SEARCH SellerProductMapping USING COVERING INDEX ProductID_SellerProductMapping_INDEX (ProductID=? AND Inventory>?)

select ProductID, Inventory, CustomerAverageReview from
	 	(select * from Product left join Category using (CategoryID)) natural join SellerProductMapping
	  	where CountryOrigin = 'United States of America' and Inventory > 250 and CustomerAverageReview > 4
	  	order by CustomerAverageReview desc;

--------------------------------------------------------------------------------------------------------
-- CREATE INDEXES
CREATE INDEX CountryOrigin_Product_INDEX ON Product (CountryOrigin, CustomerAverageReview);
CREATE INDEX ProductID_SellerProductMapping_INDEX ON SellerProductMapping (ProductID, Inventory); -- covering
--------------------------------------------------------------------------------------------------------

select ProductID, Inventory, CustomerAverageReview from
	 	(select * from Product left join Category using (CategoryID)) natural join SellerProductMapping
	  	where CountryOrigin = 'United States of America' and Inventory > 250 and CustomerAverageReview > 4
	  	order by CustomerAverageReview desc;


--------------------------------------------------------------------------------------------------------
-- DROP INDEXES
DROP INDEX CountryOrigin_Product_INDEX;
DROP INDEX ProductID_SellerProductMapping_INDEX;

--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------

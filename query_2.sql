-- Updated query.sql (added temporary table for 4th query)
--------------------------------------------------------------------------------------

-- The company is celebrating its one-year anniversary by giving away
--	gift cards to customers who have bought more than $100 so far, so
--	they need the names and emails for generating emails
select sum(PriceTotal) as TotalBought, CustomerFirstName, CustomerEmail
from Orders natural join Customer 
group by CustomerFirstName
having PriceTotal >= 100;

--------------------------------------------------------------------------------------

-- The company is interested in listing the best products from each country 
--	on their front page on 'world is one day!', for this they need the top products (IDs) and 
--	their respective countries as a list
select ProductID, CountryOrigin from
(select *, row_number() over (partition by CountryOrigin 
		  order by CustomerAverageReview*CustomerReviewsNumber) 
	as CountryRank from 
Product left outer join Category using (CategoryID))
where CountryRank = 1;

--------------------------------------------------------------------------------------

-- Using the [PCLocationsCount] view (number of postal companies serving in a specific city), 
--  the company is interested in checking sellers that are also in the same city as the 
-- 	postal company for strategic purposes, such as imposing conditions on those sellers to only
--	utilize those postal companies
select SellerID, SellerAddressCity, Number_of_Locations as PostalCompaniesInCity
from Seller join PCLocationsCount on Seller.SellerAddressCity = PCLocationsCount.City;

-- Please run populate_db.sql again (other than dropping tables part), 
-- a slight change in city has been done. Updated populate_db.sql is in p3.
-- Result shows that, there are 11 postal companies that serve in Chicago, most sellers are
--	not in the same city as the postal company (more data would produce a better result)

--------------------------------------------------------------------------------------

-- Using the [AvgProductPriceCity] view,
--  The company wishes to compare the customer's cart with the neighbourhood (city)
--	so as to show ads based on whether current carts' average is higher/lower
--	A customer with a higher cart average is willing to spend more, so push him/her to buy
--	while if a customer is not even willing to buy, why spend budget on showing ads to them!
-- but using the temporary table created belows

create temporary table AvCompareTemp as
select CustomerID, Customer.CustomerAddressCity, AvgProductPriceInCart as AvgProdPriceCity
from Customer join AvgProductPriceCity on 
Customer.CustomerAddressCity = AvgProductPriceCity.CustomerAddressCity 
where AvgProdPriceCity is not null;

-----------------

select CustomerID, CartID, CustomerAddressCity,
CASE
   WHEN CartTotal/CartProductsNumber > AvgProdPriceCity
       THEN 'Higher' 
   ELSE 'Lower' 
END CurrentCartVsCityCart

from AvCompareTemp natural join Cart order by CustomerAddressCity;

--------------------------------------------------------------------------------------

-- Using the [PaymentMethodForCity] view,
-- 	The company wants to contact customers who are not utilizing the payment (especially credits)
--	method that is used by most people in that city, so as to introduce them to
--	discounts from fintech partners.
select CustomerFirstName, CustomerEmail, City, 
PaymentMethodForCity.TopPaymentMethod as TopPaymentMethodInCity, PaymentMethod from 
(Customer join PaymentMethodForCity on Customer.CustomerAddressCity = PaymentMethodForCity.City)
natural join Orders
where TopPaymentMethodInCity <> PaymentMethod;

--------------------------------------------------------------------------------------

-- The company is interested in knowing the categories that are most reviewed, they are hoping
--	to acquire SMBs in these verticals
select CategoryName, ReviewAverageCount from
(select CustomerReviewsNumber, ProductID, CategoryName, 
avg(CustomerReviewsNumber) over(partition by CategoryID) as ReviewAverageCount 
from Product natural join Category)
group by CategoryName having ReviewAverageCount > 400
order by ReviewAverageCount desc;

--------------------------------------------------------------------------------------

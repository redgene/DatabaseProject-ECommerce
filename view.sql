--------------------------------------------------------------------------------------

-- The company frequently needs to check the states where there are enough 
--	postal companies serving. So that more companies
--	can be onboarded as per requirements if this count is low
create view PCLocationsCount as
select PostalCompanyLocation as City, count(*) as Number_of_Locations
from PostalCompanyServingLocations group by PostalCompanyLocation
order by Number_of_Locations desc;

--------------------------------------------------------------------------------------

-- The company also needs to check the average price per product in the customer's cart
--	grouped by city for survey purposes, the higher average price per product is an indication
--	of purchasing power parity
create view AvgProductPriceCity as
select CustomerAddressCity, avg(ratio) as AvgProductPriceInCart from
(select CartTotal/CartProductsNumber as ratio, CustomerAddressCity 
from Cart natural join Customer)
group by CustomerAddressCity;

--------------------------------------------------------------------------------------

-- The company is interested in understanding the payment methods used by 
--	people in different cities, so that they can push their credit card plans
create view PaymentMethodForCity as
select * from(
select CustomerAddressCity as City, max(FrequencyOfPayMethod) as UsageFrequency, 
PaymentMethod as TopPaymentMethod from
( select Customer.CustomerID, CustomerAddressCity, PaymentMethod,
count(*) over(partition by CustomerAddressCity, PaymentMethod) as FrequencyOfPayMethod
from Orders join Customer on Customer.CustomerID =  Orders.CustomerID 
) group by City  );

--------------------------------------------------------------------------------------
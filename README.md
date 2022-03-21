# Databases Project - ECommerce
Retail E-Commerce sales show a strong upward trend [1]. Therefore for this project, the aim is to create a relational database for a new e-commerce startup 
Based on the current design, there are 8 entities (namely: Product, Order, Seller, Inventory, Customer, Cart, Postal_Company, Category) with 10+ relations. 
This has been shown below the description as well.

- Product: For a specific product, details such as its unique Product ID, country of origin, price (new + old), seller ID, category ID etc., can to be added.
- Order: For a specific order, its unique Order ID, seller ID(s), customer ID, payment method, delivery dates (expected + actual), shipping company etc.
- Seller: There can be multiple sellers that sell a specific product and vice versa (multiple products sold by same seller). These entities (Product and Seller) 
are expected to be linked via their IDs, with Seller entity containing details about a seller.
- Inventory stores number of units available against each product ID and seller ID.
- Customer maps customer ID with order ID and contains other details such as default address, phone, name etc.
- Cart entity contains all customers that have a non-empty cart and maps customer ID with product ID.
- PostalCompany: As noticed, different sellers use different postal companies (UPS, FedEx, DHL etc.) depending on the products and address to be shipped to. 
Hence, each Order and Seller is expected  to contain Postal company ID; where the details for each company is available in PostalCompany entity, 
which could also store the locations where the company serves. If possible, the target and source location can be optimized based on a standard price ($/km). 
Postal company’s success rate can also be factored in.
- Category of the product is another important aspect, as noticed on websites. Since, users also may want to search all products in a given category.
Hence, this product ID - category ID mapping is stored in Category entity.
[1] statista.com/statistics/379046/worldwide-retail-e-commerce-sales

![ERD](https://github.com/redgene/DatabaseProject-ECommerce/blob/main/ERD.png)

# Webapplication (bottle framework python)
- Python script uses the same ecommerce.db.
- Most instructions have been provided on the web-page itself, and error checking has been implemented.

Product Search, Product Insertion, Product Deletion, Product Updation, Product: Seller Insertion, Product: Seller Linkage, etc have been implemented.

## Product Insertion + Deletion
![Product_InsDel](https://github.com/redgene/DatabaseProject-ECommerce/blob/main/screenshots/Product_Insertion_Deletion.gif)

## Product Updation
![Product_Upd](https://github.com/redgene/DatabaseProject-ECommerce/blob/main/screenshots/Product_Updation.gif)

## Seller Insertion for Product
![Product_SellerIns](https://github.com/redgene/DatabaseProject-ECommerce/blob/main/screenshots/Product_SellerInsert.gif)

## Seller Linking for Product
![Product_SellerIns](https://github.com/redgene/DatabaseProject-ECommerce/blob/main/screenshots/Product_SellerLink.gif)

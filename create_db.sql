CREATE TABLE "Customer" (
	"CustomerID"			TEXT NOT NULL,
	"CustomerFirstName"		TEXT NOT NULL,
	"CustomerLastName"		TEXT,
	"CustomerAddressStreet"	TEXT,
	"CustomerAddressCity"	TEXT,
	"CustomerAddressState"	TEXT,
	"CustomerAddressZip"	TEXT,
	"CustomerPhone"			TEXT NOT NULL,
	"CustomerEmail"			TEXT NOT NULL,
	PRIMARY KEY("CustomerID")
);

CREATE TABLE "Category" (
	"CategoryID"			TEXT NOT NULL,
	"CategoryName"			TEXT NOT NULL,
	"CategoryPercentShare"	REAL NOT NULL,
	PRIMARY KEY("CategoryID")
);

CREATE TABLE "Product" (
	"ProductID"				TEXT NOT NULL,
	"Brand"					TEXT NOT NULL,
	"MaterialColorCapacity"	TEXT,
	"CountryOrigin"			TEXT,
	"CustomerReviewsNumber"	INTEGER,
	"CustomerAverageReview"	REAL,
	"PriceNew"				REAL,
	"PriceUsed"				REAL,
	"CategoryID"			TEXT,
	PRIMARY KEY("ProductID"),
	FOREIGN KEY("CategoryID") REFERENCES "Category"("CategoryID")
);

CREATE TABLE "Seller" (
	"SellerID"				TEXT NOT NULL,
	"SellerEmail"			TEXT NOT NULL,
	"SellerPhone"			TEXT,
	"SellerAddressStreet"	TEXT,
	"SellerAddressCity"		TEXT,
	"SellerAddressState"	TEXT,
	"SellerAddressZip"		TEXT,
	PRIMARY KEY("SellerID")
);

CREATE TABLE "SellerProductMapping" (
	"SellerID"	TEXT,
	"ProductID"	TEXT,
	"Inventory"	INTEGER NOT NULL,
	FOREIGN KEY("ProductID") REFERENCES "Product"("ProductID"),
	FOREIGN KEY("SellerID") REFERENCES "Seller"("SellerID")
);

CREATE TABLE "PostalCompany" (
	"PostalCompanyID"	TEXT NOT NULL,
	"PostalCompanyName"	TEXT NOT NULL,
	"PostalCompanyHQ"	TEXT,
	PRIMARY KEY("PostalCompanyID")
);

CREATE TABLE "PostalCompanyServingLocations" (
	"PostalCompanyID"		TEXT,
	"PostalCompanyLocation"	TEXT,
	FOREIGN KEY("PostalCompanyID") REFERENCES "PostalCompany"("PostalCompanyID")
);

CREATE TABLE "SellerPostalCompanyMapping" (
	"SellerID"			TEXT,
	"PostalCompanyID"	TEXT,
	FOREIGN KEY("SellerID") REFERENCES "Seller"("SellerID"),
	FOREIGN KEY("PostalCompanyID") REFERENCES "PostalCompany"("PostalCompanyID")
);

CREATE TABLE "Orders" (
	"OrderID"				TEXT NOT NULL,
	"PaymentMethod"			TEXT NOT NULL,
	"PriceTotal"			REAL NOT NULL,
	"DeliverDateExpected"	TEXT NOT NULL,
	"DeliveryDateActual"	TEXT,
	"PostalCompanyID"		TEXT,
	"SellerID"				TEXT,
	"CustomerID"			TEXT NOT NULL,
	FOREIGN KEY("PostalCompanyID")  REFERENCES "PostalCompany"("PostalCompanyID"),
	FOREIGN KEY("CustomerID") 		REFERENCES "Customer"("CustomerID"),
	FOREIGN KEY("SellerID") 		REFERENCES "Seller"("SellerID"),
	PRIMARY KEY("OrderID")
);

CREATE TABLE "ProductRelatedItems" (
	"ProductID1"	TEXT,
	"ProductID2"	TEXT,
	FOREIGN KEY("ProductID1") REFERENCES "Product"("ProductID"),
	FOREIGN KEY("ProductID2") REFERENCES "Product"("ProductID")
);

CREATE TABLE "Cart" (
	"CartID"				TEXT NOT NULL,
	"CartTotal"				REAL NOT NULL,
	"CartProductsNumber"	INTEGER NOT NULL,
	"CustomerID"			TEXT,
	PRIMARY KEY("CartID"),
	FOREIGN KEY("CustomerID") REFERENCES "Customer"("CustomerID") -- each customer has 1:1 mapping with a cart
);

CREATE TABLE "ProductsInCart" (
	"ProductID"	TEXT,
	"CartID"	TEXT,
	FOREIGN KEY("CartID")    REFERENCES "Cart"("CartID"),
	FOREIGN KEY("ProductID") REFERENCES "Product"("ProductID")
);

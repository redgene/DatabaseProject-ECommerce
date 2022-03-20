-- schemamodification


-- Altering table to add a column
ALTER TABLE Product
ADD ProductDescription TEXT;

-- Altering table to drop a column
ALTER TABLE Cart
DROP COLUMN CartTotal;

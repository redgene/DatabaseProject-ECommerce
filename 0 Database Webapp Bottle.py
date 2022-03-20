from bottle import route, run, template, post, get, request
import sqlite3

# In the same folder as python script
con = sqlite3.connect('ecommerce.db') 
cur = con.cursor()
cur2 = con.cursor()

product_form_instructions = \
"Checks will be done from top to bottom and the error that's encountered first will be returned if any <br>\
<br><b>Rules for adding a product:</b><br>\
1. ProductID can't be empty & should be of the form XX-YYYYYYYY where X:Alphabet Y: Number<br>\
2. Brand can't be empty<br>\
3. If entered, CountryOrigin should be one of those in the list<br>\
4. If entered, CustomerReviewsNumber should be a whole number<br>\
5. If entered, CustomerAverageReview should be a float between 0 and 5 inclusive<br>\
6. If entered, CustomerReviewsNumber and CustomerAverageReview can both be 0, and both be non-zero<br>\
7. If entered, PriceNew and PriceOld should be positive numbers, can be floats + can't be empty<br>\
8. If entered, CategoryID should be one of those in the list <br><br>"

seller_form_instructions = \
"Checks will be done from top to bottom and the error that's encountered first will be returned if any <br>\
<br><b>Rules for adding a seller:</b><br>\
1. SellerID can't be empty & should be of the form XXXX-YYYY where X:Alphabet Y: Number<br>\
2. EmailID  can't be empty & should have a form string1@string2.string3<br>\
3. If entered, Phone number should be at least 10 digits, ignoring the special characters<br>\
4. If entered, SellerAddressCity and SellerAddressState should only be alphabets. Spaces are allowed<br>\
5. If entered, SellerAddressZip should be a 5-digit number<br>\
6. If entered, Inventory should be a whole number<br>"

@route('/')
def begin():

    html =  '<h1><p align="center"> E-Commerce: Product-Seller Platform </p></h1>'

    # Insertion (Product)
    html += "<h1> Insert a new Product</h1>"
    html += "<a href = \"/insert_product_form_show\"> Insert Product in the Product List </a> <br><br>"

    html+= "As a user, I would want to buy products with at least one seller - this is what the second form does <br>"
    html+= "Please note that a new product inserted won't appear in the search results of the second form <br>"
    html+= "For ease, there are two forms for searching products below <br>"
    html+= "Therefore, <font color = 'red'> <b>use the first form to search for the newly inserted product</b></font> <br>"
    html+= "But since <font color = 'red'>the results need to be capped, consider narrowing down using the search attributes if newly inserted product doesn't appear in the first go </font>"
    html+= "<br>For example, a product inserted for country 'Angola' might not appear in the results, but would appear if CategoryID is also mentioned. "
    html+= "since it's inserted at the end of the table"

    # Search (Product)
    html += "<h1> Search in the Products Table </h1>"
    html += "Following lists can be used for efficient search:"
    html += '''
    <ul>
      <li><a href = \"/all_countries\"> Click here to see Country list </a><br></li>
      <li><a href = \"/all_categories\"> Click here to see CategoryID List </a><br></li>
      <li><a href = \"/all_brands\"> Click here to see Top Brands list </a><br></li>
    </ul>
    '''

    html += "<h3>Search Products - Useful for checking / adding sellers right after inserting new product(s)</h3>"

    # Add example with most products for that country
    html += "Example: Brand = Cox"
    html += "<br>Example: Country = Angola"
    html += "<br>Example: CategoryID = CFA"

    # Second form for showing all products (especially for adding sellers to products that were added recently)
    html += '''
    <form action = "/search_product/full" method = "post">
      <table>
        <tr>
          <td align="right">Brand*:</td>
          <td align="left"><input type="text" name="Brand" /></td>
        </tr>
        <tr>
          <td align="right">CountryOrigin:</td>
          <td align="left"><input type="text" name="CountryOrigin" /></td>
        </tr>
        <tr>
          <td align="right">CategoryID:</td>
          <td align="left"><input type="text" name="CategoryID" /></td>

        </tr>

      </table>
      <input value = "Search all products matching these constraints" type = "submit" />
    </form>
    '''

    html+= "Please note that a newly added product might not appear in this form below, since there were no sellers added yet <br>"
    html+= "Please search using the first form above for all products to appear, and not sorted by number of sellers"

    html += "<h3>Search for Products with >=1 Seller(s)</h3>"

    # HTML Form for Searching Product
    html += '''
    <form action = "/search_product/limited" method = "post">
      <table>
        <tr>
          <td align="right">Brand*:</td>
          <td align="left"><input type="text" name="Brand" /></td>
        </tr>
        <tr>
          <td align="right">CountryOrigin:</td>
          <td align="left"><input type="text" name="CountryOrigin" /></td>
        </tr>
        <tr>
          <td align="right">CategoryID:</td>
          <td align="left"><input type="text" name="CategoryID" /></td>

        </tr>

      </table>
      <input value = "Search Products (at least 1 Seller)" type = "submit" />
    </form>
    '''

    # -- Part removed, since not expected

    # html += "<h2>Link an existing product to an existing seller</h2>"
    # html += "<a href = \"/top_sellers\"> > Click here to see top sellers as examples </a> <br>"
    # html += "Inventory should be a natural integer (>=1) and SellerID should be one of those already in the Sellers Table"
    # html += "<br> None of them should be empty" 

    # # HTML Form for Linking Seller with Product
    # html += '''
    # <form action = "/link_seller_product" method = "post"><br>
    #   <table>
    #     <tr><td align="right">SellerID: </td><td align="left"><input type="text" name="SellerID" /></td></tr>
    #     <tr><td align="right">ProductID:</td><td align="left"><input type="text" name="ProductID" /></td></tr>
    #     <tr><td align="right">Inventory:</td><td align="left"><input type="text" name="Inventory" /></td></tr>

    #   </table>
    #   <input value = "Link Seller & Product" type = "submit"  />
    # </form>
    # '''


    return html
    # Example Product
    # ('JD-17629186','Roberts-Rasmussen','#9f2cdd', 'Montserrat', '864', '4.52', '559.52', '526.65', 'CFA'),

# Helper function to get the number of sellers for a product - so that only products can be narrowed down
#   based on number of sellers (0 or more)
def getSellers(val):
    num_sellers_query = "select count(*) from SellerProductMapping where ProductID = '{}';".format(val)
    num_sellers_query_out = cur2.execute(num_sellers_query)

    num_sellers = ""
    for rowX in num_sellers_query_out:
        for cellX in rowX:
            num_sellers = str(cellX)

    return num_sellers

# Search Helper Function with redirecting links to update/delete record
@route ('/search_product/<val>', method='POST')
def search_product(val):
    Brand                  = request.forms.get("Brand")
    CountryOrigin          = request.forms.get("CountryOrigin")
    CategoryID             = request.forms.get("CategoryID")

    ## CHECK FOR COUNTRY OF ORIGIN BEFORE MOVING FORWARD
    ## SHOULD BE ONE IN THE LIST
    countries = set()
    sql_query_output = cur.execute("select CountryOrigin from Product group by CountryOrigin;")
    for row in sql_query_output:
        for cell in row:
            countries.add (str(cell))


    ## CHECK FOR CATEGORYID BEFORE MOVING FORWARD
    categories = set()
    sql_query_output = cur.execute("select CategoryID from Category;")
    for row in sql_query_output:
        for cell in row:
            categories.add (str(cell))

    if CountryOrigin not in countries and len(CountryOrigin) != 0 and CategoryID not in categories and len(CategoryID) != 0:
        return "Sorry, the country and the CategoryID you have entered do not exist! Please update the fields"

    if CountryOrigin not in countries and len(CountryOrigin) != 0:
        return "Sorry, the country you have added does not exist! Please update the field, see the main list of countries again"

    if CategoryID not in categories and len(CategoryID) != 0:
        return "Sorry, the categoryID you have added does not exist! Please update the field, see the main list of categories again"

    # 8 Cases:
    # Brand                  | Y | Y | N | Y | N | Y | N | N |
    # CountryOrigin          | Y | Y | Y | N | Y | N | N | N |
    # CategoryID             | Y | N | Y | Y | N | N | Y | N |

    l1, l2, l3 = True if len (Brand) > 0 else False, \
                 True if len (CountryOrigin) > 0 else False, \
                 True if len (CategoryID) > 0 else False

    # FILL sql_query BASED ON THE USER INPUTS
    sql_query = ""

    # l1 --> Brand
    # l2 --> CountryOrigin
    # l3 --> CategoryID
    
    # Showing only those products that have at least one seller for the 'limited' option
    # Since if a customer can't buy, there is no point of showing the product

    q = ""

    if val == 'limited':
        q = "select ProductID, Brand, CountryOrigin, CustomerReviewsNumber, CustomerAverageReview, PriceNew, CategoryID\
        from Product natural join SellerProductMapping group by ProductID having count(*) > 0 order by count(*) desc"

    # No limitations on the number of sellers --> better for checking added product
    else:
        q = "select ProductID, Brand, CountryOrigin, CustomerReviewsNumber, CustomerAverageReview, PriceNew, CategoryID from Product"
    
    # 8 Cases:
    if l1 and l2 and l3:
        sql_query = "select * from ({}) where Brand like '%{}%' and CountryOrigin = '{}' and CategoryID = '{}' limit 20". format (q, Brand, CountryOrigin, CategoryID)

        # if val == 'limited':
        #     sql_query = "select * from ({}) where Brand like '%{}%' and CountryOrigin = '{}' and CategoryID = '{}' limit 20". format (q, Brand, CountryOrigin, CategoryID)
        # else:
        #     sql_query = "select * from ({}) where Brand like '%{}%' and CountryOrigin = '{}' and CategoryID = '{}' limit 20". format (q, Brand, CountryOrigin, CategoryID)

    if l1 and l2 and not l3:
        sql_query = "select * from ({}) where Brand like '%{}%' and CountryOrigin = '{}' limit 20". format (q, Brand, CountryOrigin)
        # if val == 'limited':
        #     sql_query = "select * from ({}) where Brand like '%{}%' and CountryOrigin = '{}' limit 20". format (q, Brand, CountryOrigin)

        # else:
        #     sql_query = "select * from ({}) where Brand like '%{}%' and CountryOrigin = '{}' limit 20". format (q, Brand, CountryOrigin)            

    if not l1 and l2 and l3:
        sql_query = "select * from ({}) where CountryOrigin = '{}' and CategoryID = '{}' limit 20". format (q, CountryOrigin, CategoryID)
        # if val == 'limited':
        #     sql_query = "select * from ({}) where CountryOrigin = '{}' and CategoryID = '{}' limit 20". format (q, CountryOrigin, CategoryID)
        # else:
        #     sql_query = "select * from ({}) where CountryOrigin = '{}' and CategoryID = '{}' limit 20". format (q, CountryOrigin, CategoryID)

    if l1 and not l2 and l3:
        sql_query = "select * from ({}) where Brand like '%{}%' and CategoryID = '{}' limit 20". format (q, Brand, CategoryID)

        # if val == 'limited':
        #     sql_query = "select * from ({}) where Brand like '%{}%'' and CategoryID = '{}' limit 20". format (q, Brand, CategoryID)
        # else:
        #     sql_query = "select * from ({}) where Brand like '%{}%' and CategoryID = '{}' limit 20". format (q, Brand, CategoryID)            


    if not l1 and l2 and not l3:
        sql_query = "select * from ({}) where CountryOrigin = '{}' limit 20". format (q, CountryOrigin)        
        # if val == 'limited':
        #     sql_query = "select * from ({}) where CountryOrigin = '{}' limit 20". format (q, CountryOrigin)

        # else:
        #     sql_query = "select * from ({}) where CountryOrigin = '{}' limit 20". format (q, CountryOrigin)            

    if l1 and not l2 and not l3:
        sql_query = "select * from ({}) where Brand like '%{}%' limit 20". format (q, Brand)
        # if val == 'limited':
        #     sql_query = "select * from ({}) where Brand like '%{}%' limit 20". format (q, Brand)
        # else:
        #     sql_query = "select * from ({}) where Brand like '%{}%' limit 20". format (q, Brand)


    if not l1 and not l2 and l3:
        sql_query = "select * from ({}) where CategoryID = '{}' limit 20". format (q, CategoryID)
        # if val == 'limited':
        #     sql_query = "select * from ({}) where CategoryID = '{}' limit 20". format (q, CategoryID)
        # else:
        #     sql_query = "select * from ({}) where CategoryID = '{}' limit 20". format (q, CategoryID)


    if not l1 and not l2 and not l3:
        sql_query = "select * from ({}) limit 20". format (q)
        # if val == 'limited':
        #     sql_query = "select * from ({}) limit 20". format (q, Brand, CountryOrigin, CategoryID)
        # else:
        #     sql_query = "select * from ({}) limit 20". format (q, Brand, CountryOrigin, CategoryID)


    GivenInputs = "Searching for CountryOrigin: {}, Brand: {}, CategoryID: {} </br>".format(\
        CountryOrigin if len(CountryOrigin)>0 else "NO CONSTRAINTS",\
        Brand         if len(Brand)>0         else "NO CONSTRAINTS",\
        CategoryID    if len(CategoryID)>0    else "NO CONSTRAINTS")

    html = '''<style> table, th, td { border: 1px solid black;}</style>'''
    html += "<h2> Product Search Results </h2>"
    html += GivenInputs

    sql_query_output = cur.execute(sql_query)

    html += '''
      <table>
         <tr>
            <th>ID</th><th>Brand</th><th>Country Origin</th><th>Reviews Number</th><th>Avg Rating</th><th>Price-New</th>
            <th>Category</th><th>SellersNumber</th>
         </tr>
    '''

    # CHECK: IF THERE ARE ANY RESULTS AT ALL
    # IF there are none, show a message instead of showing an empty table!
    check_output_size = []

    for row in sql_query_output:
        html += "<tr>"

        for cell in row:
            html += "<td>" + str(cell) + "</td>"
            check_output_size.append (str(cell))
        num_sellers = getSellers (row[0])

        # Add number of sellers to the table
        html += "<td>" + num_sellers + "</td>"

        # Redirect button for viewing / updating records
        html += "<td><a href=\"/view_update_product/" + row[0] + "\">View/Update</a> </td>"

        # Redirect button for deleting records
        html += "<td><a href=\"/delete_product/" + row[0] + "\">Delete</a> </td>"

        # Redirect button for checking sellers
        html += "<td><a href=\"/sellers_for_product/" + row[0] + "\">Show Sellers</a> </td>"

        # Redirect button for adding seller to a product
        html += "<td><a href=\"/insert_seller_for_product_form_show/" + row[0] + "\">Add Seller</a> </td>  </tr>"

    
    if len(check_output_size) == 0:
        return "Sorry, there are no Results to be displayed, please re-run the search with wider parameters."

    html += "</table>"
    html += "<br /><br /><br /><br /><br />"

    return html

# -----------------------------------------------------------------------------------------------

# For storing old product details while updating
class OldProductDetails(object):
    """Storing details of a product before updating it"""
    def __init__(self, arg):
        # arg is a list of all details, which is updated everytime
        self.arg = arg 

# Class object for accessing details
oldP = OldProductDetails ([])

lst_seller = []     # For storing old seller details

# Helper functions to check ProductID entered by the User
def check_ProductID (s):
    if s.count('-') != 1:
        return False
        
    letters, digits = s.split('-')
    if len(letters)!= 2 or len(digits)!= 8:
        return False
        
    if not letters.isalpha() or not digits.isnumeric():
        return False
    
    return True 

# Helper functions to check Product Reviews / Ratings entered by the User
def check_reviews (num, rating): #-- check for 3..3 (2 dots!)
    # isdigit works with +/0 only
    
    if rating.count('.') == 1: # 3.4 rating
        before, after = rating.split('.')
        if not before.isdigit() or not after.isdigit():
            return False
            
    elif rating.count('.') == 0:
        if not rating.isdigit():
            return False
    
    if not num.isdigit():
        return False
    
    num = int(num)
    rating = float(rating)

    if num < 0 or rating < 0 or rating > 5:
        return False
    if (num == 0 and rating != 0) or (num !=0 and rating == 0):
        return False
    return True

# Helper functions to check Product Prices entered by the User
def check_price (p):
    if len(p) > 0:
        if p.count('.') == 1:
            before, after = p.split('.')
            if not before.isdigit() or not after.isdigit():
                return False

        elif p.count('.') == 0 and not p.isdigit():
                return False

        elif p.count('.') > 1:
            return False
            
    return True

# MAIN HELPER FUNCTION RELIES ON 3 FUNCTIONS DEFINED ABOVE
#  IMPLEMENTS CHECKS BEFORE INSERTING / UPDATING A PRODUCT
def Product_CHECK (ProductID, OldProductID, Brand,\
                   CustomerAverageReview, CustomerReviewsNumber, \
                   CountryOrigin, CategoryID, PriceNew, PriceUsed, updating, adding):

    # NULL CHECK [1]
    if len(ProductID) == 0 or len(Brand) == 0:
        return "Sorry, the ProductID or Brand cannot be empty.\
        Enter either the old ones, or update them please."

    # MAPPING UPDATE [2]
    if OldProductID:
        if ProductID != OldProductID:
            cur.execute ("UPDATE SellerProductMapping SET ProductID = '{}'\
            where ProductID = '{}';".format (ProductID, OldProductID))
            con.commit()

    # ID should not be repeated (since it's unique) [3]
    sql_query_output = cur.execute("select ProductID from Product where ProductID = '{}';".format(ProductID))

    # print(sql_query_output)
    prodcheck = []
    for row in sql_query_output:
        for cell in row:
            # print(str(cell))
            prodcheck.append (str(cell))

    # if we are updating a product
    if updating:
        if len(prodcheck) > 0 and OldProductID and OldProductID not in prodcheck:
            return "Sorry, the ProductID you have entered is already present in the table, please provide a new product ID / keep it same as before!"

    # if we are adding a product
    if adding:
        if len(prodcheck) > 0 and ProductID in prodcheck:
            return "Sorry, the ProductID you have entered is already present in the table, please provide a new product ID / keep it same as before"


    # ID Specific Structure Check
    if not check_ProductID(ProductID):
        return "Sorry, the ProductID does not match the constraints, it needs to be of the form XX-YYYYYYYY"


    # Customer Reviews Number and Rating Check
    # Also possble that the user does not enter anything in the reviews fields
    # In that case, either of them can be considered 0 or 0.0

    CustomerAverageReview = "0" if len(CustomerAverageReview) == 0 else CustomerAverageReview
    CustomerReviewsNumber = "0" if len(CustomerReviewsNumber) == 0 else CustomerReviewsNumber

    if not check_reviews(CustomerReviewsNumber, CustomerAverageReview):
        return "Sorry, please check the rating / number of ratings entered"

    if not check_price(PriceNew) or not check_price(PriceUsed):
        return "Sorry, please check the Prices entered"


    ## CHECK FOR COUNTRY OF ORIGIN & CATEGORYID BEFORE MOVING FORWARD
    countries = set()
    sql_query_output = cur.execute("select CountryOrigin from Product group by CountryOrigin;")
    for row in sql_query_output:
        for cell in row:
            countries.add (str(cell))

    categories = set()
    sql_query_output = cur.execute("select CategoryID from Category;")
    for row in sql_query_output:
        for cell in row:
            categories.add (str(cell))

    if CountryOrigin not in countries and len(CountryOrigin) != 0 and CategoryID not in categories and len(CategoryID) != 0:
        return "Sorry, the country and the CategoryID you have entered do not exist! Please update the fields"


    if CountryOrigin not in countries and len(CountryOrigin) != 0:
        return "Sorry, the country you have added does not exist! Please update the field, see the main list of countries again"


    if CategoryID not in categories and len(CategoryID) != 0:
        return "Sorry, the categoryID you have added does not exist! Please update the field, see the main list of categories again"
    
    return True

# MAIN HELPER FUNCTION TO CHECK BEFORE ADDING A SELLER
def Seller_CHECK (SellerID, SellerEmail, SellerPhone, \
                  SellerAddressCity, SellerAddressState,\
                   SellerAddressZip, Inventory):

    ######################## SELLER ID ########################
    if len(SellerID) == 0:
        return "SellerID can't be empty"

    # SELLERID - FORMATTING CHECK
    if SellerID.count ('-') != 1 :
        return "Check SellerID - needs to be formatted as ZZZZ-YYYY, where Z: Letter, Y: Number"    

    before, after = SellerID.split('-') # DIFO-9898
    if not before.isalpha() or not after.isdigit() or \
        not len(before) == 4 or not len(after) == 4:
        return "Check SellerID - needs to be formatted as ZZZZ-YYYY, where Z: Letter, Y: Number"
    
    # SELLER_ID UNIQUENESS CHECK
    sql_query_output = cur.execute("select SellerID from Seller where SellerID = '{}';".format(SellerID))

    # print(sql_query_output)
    sellercheck = []
    for row in sql_query_output:
        for cell in row:
            # print(str(cell))
            sellercheck.append (str(cell))

    if len(sellercheck) > 0:
        return "This SellerID is already present in the table, please update!"

    # SELLER EMAIL CHECK HAS BEEN AUTOMATED VIA HTML ITSELF
    if len(SellerEmail) == 0:
        return "EmailID field can't be empty"

    ######################## SELLER PHONE ####################################
    # SELLER PHONE, IF ENTERED SHOULD HAVE 10 DIGITS (IGNORING THE SPECIAL CHARACTERS)
    if len(SellerPhone) > 0:
        temp = ''
        for ch in SellerPhone:
            if ch.isdigit():
                temp += ch

        if len (temp) < 10:
            return "Seller's Phone should have at least 10 digits"

    ######################## SELLER CITY AND STATE #############################
    # SELLER CITY, STATE SHOULD NOT HAVE ANY SPECIAL CHARACTERS OTHER THAN SPACES
    tempcity, tempstate = SellerAddressCity.replace(' ', ''), SellerAddressState.replace(' ', '')

    if len(tempcity) > 0 and not tempcity.isalpha():
        return "The seller's city should consist of alphabets (spaces allowed)"

    if len(tempstate) > 0 and not tempstate.isalpha():
        return "The seller's state should consist of alphabets (spaces allowed)"


    ######################## SELLER ZIP ########################
    # SELLER ZIP SHOULD BE 5 DIGITS, AS ALL SELLERS ARE LOCATED IN THE US
    if len(SellerAddressZip) > 0:
        if len (SellerAddressZip) != 5 or not SellerAddressZip.isdigit():
            return "The seller's zip-code should only be 5 digits"

    # INVENTORY VALUE CHECK
    if Inventory and len(Inventory) > 0:
        if not Inventory.isdigit():
            return "Check Inventory Value"
        
        if int(Inventory) < 1:
            return "Check Inventory Value"
        
    return True
# -----------------------------------------------------------------------------------------------

# Product Updation Helper Functions
@route('/view_update_product/<ProductID>')
def view_update_product(ProductID):
    html = "<style>table, th, td {border: 1px solid black;}</style>"
    html += "<h2> Viewing / Updating the Product with ProductID: {} </h2>".format(ProductID)

    # show the output again but also give a form below it to update this record
    sql_query_output = cur.execute("select * from Product where ProductID = '" + ProductID + "'")
    html += '''
      <table>
         <tr>
            <th>ID</th><th>Brand</th><th>Color</th><th>Origin</th><th>Reviews</th><th>Rating</th><th>Price-New</th><th>Price-Old</th><th>Category</th>
         </tr>
    '''

    lst = []
    for row in sql_query_output:
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
            lst.append (str (cell))

    oldP.arg = lst # UPDATE THE OBJECT

    html += "</table><br/>"
    html += "<h2> Please use the following Form to Update this Product</h2>"
    html += "<h3> Details have already been filled out, but feel free to change as required, following the rules</h3>"

    html += product_form_instructions

    html += "<br> Please note that the ProductID will NOT be editable."
    # Initial version supported editing the productID as well (which happens to be the primary key)
    # For revert back to this version, can simply remove the constraint readonly below and make the field editable again in the following form!

    # HTML Form for updating Product
    html += '''
    <form action = "/update_product" method = "post"><br>
      <table>
        <tr><td align="right">ProductID:</td><td align="left"><input type="text" name="ProductID" value = "{}"  readonly/></td></tr>
        <tr><td align="right">Brand:</td><td align="left"><input type="text" name="Brand" value = "{}" /></td></tr>
        <tr><td align="right">MaterialColorCapacity:</td><td align="left"><input type="text" name="MaterialColorCapacity"  value = "{}"  /></td></tr>
        <tr><td align="right">CountryOrigin:</td><td align="left"><input type="text" name="CountryOrigin"  value = "{}"  /></td></tr>
        <tr><td align="right">CustomerReviewsNumber:</td><td align="left"><input type="text" name="CustomerReviewsNumber"  value = "{}"  /></td></tr>
        <tr><td align="right">CustomerAverageReview:</td><td align="left"><input type="text" name="CustomerAverageReview"  value = "{}"  /></td></tr>
        <tr><td align="right">PriceNew:</td><td align="left"><input type="text" name="PriceNew"  value = "{}"  /></td></tr>
        <tr><td align="right">PriceUsed:</td><td align="left"><input type="text" name="PriceUsed"  value = "{}"  /></td></tr>
        <tr><td align="right">CategoryID:</td><td align="left"><input type="text" name="CategoryID"  value = "{}"  /></td></tr>
      </table>
      <input value = "Update Product" type = "submit"  />
    </form>
    '''.format (lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7], lst[8])

    return html

@route('/update_product', method = 'POST')
def update_product():

    # Old ProductID // Old product details are in the class object
    OldProductID           = oldP.arg[0]

    # ALL THE NEW / UPDATED TERMS
    ProductID              = request.forms.get("ProductID")
    Brand                  = request.forms.get("Brand")
    MaterialColorCapacity  = request.forms.get("MaterialColorCapacity")
    CountryOrigin          = request.forms.get("CountryOrigin")
    CustomerReviewsNumber  = request.forms.get("CustomerReviewsNumber")
    CustomerAverageReview  = request.forms.get("CustomerAverageReview")
    PriceNew               = request.forms.get("PriceNew")
    PriceUsed              = request.forms.get("PriceUsed")
    CategoryID             = request.forms.get("CategoryID")

    # PERFORM ALL CHECKS ON ENTERED DETAILS
    ret = Product_CHECK(ProductID, OldProductID, Brand,\
                   CustomerAverageReview, CustomerReviewsNumber, \
                   CountryOrigin, CategoryID,
                   PriceNew, PriceUsed, True, False)

    if ret != True: # If there was some error, return that error on html
        return ret

    # Initial implementation - where old details were taken
    # It is possible that the user wants to update specific details ONLY
    #   In that case, we simply take those that are to be updated, otherwise take the old ones

    # ProductID              = ProductID if len(ProductID) >0 else lst[0]
    # Brand                  = Brand if len(Brand) > 0 else lst[1]

    # MaterialColorCapacity  = MaterialColorCapacity if len(MaterialColorCapacity)>0 else oldP.arg[2]
    # CountryOrigin          = CountryOrigin         if len(CountryOrigin) >0        else oldP.arg[3]
    # CustomerReviewsNumber  = CustomerReviewsNumber if len(CustomerReviewsNumber)>0 else oldP.arg[4]
    # CustomerAverageReview  = CustomerAverageReview if len(CustomerAverageReview)>0 else oldP.arg[5]
    # PriceNew               = PriceNew              if len(PriceNew)>0              else oldP.arg[6]
    # PriceUsed              = PriceUsed             if len(PriceUsed) >0            else oldP.arg[7]
    # CategoryID             = CategoryID            if len(CategoryID)>0            else oldP.arg[8]

    # Update the details if no errors found
    cur.execute("UPDATE Product SET \
            ProductID = '{}',\
            Brand ='{}', MaterialColorCapacity = '{}', CountryOrigin = '{}', CustomerReviewsNumber = '{}',\
            CustomerAverageReview = '{}', PriceNew = '{}', PriceUsed = '{}',\
            CategoryID = '{}' where ProductID = '{}'".format\
                                                (ProductID, Brand, MaterialColorCapacity,\
                                                 CountryOrigin, CustomerReviewsNumber,\
                                                 CustomerAverageReview, PriceNew,\
                                                 PriceUsed, CategoryID, \
                                                 OldProductID))

    con.commit()

    view_update_product

    html = "<td><a href=\"/view_update_product/" + ProductID + "\">See the changes</a> </td>"
    html += OldProductID + " Updated </br> return to main <a href = \"/\">page</a>"

    return html

# -----------------------------------------------------------------------------------------------

# Product Deletion Helper Function
@route('/delete_product/<ProductID>')
def delete_product(ProductID):

    # Delete that specific product from the Product table
    cur.execute("DELETE FROM Product WHERE ProductID = '" + ProductID + "'")

    # Delete this from all the carts this product is in (since it's no longer available)
    cur.execute("DELETE FROM ProductsInCart WHERE ProductID = '" + ProductID + "'")

    # Delete this from the RelatedProducts table - and since this is two sided
    #   Product1 may be related to Product2 and vice versa - need to delete all such relations
    cur.execute("DELETE FROM ProductRelatedItems WHERE ProductID1 = '" + ProductID + "'")
    cur.execute("DELETE FROM ProductRelatedItems WHERE ProductID2 = '" + ProductID + "'")

    # Delete this from the SellerProductMapping - since those sellers can no longer sell that product
    cur.execute("DELETE FROM SellerProductMapping WHERE ProductID = '" + ProductID + "'")

    con.commit()
    return ProductID + " has been deleted </br> Click here to return to the home-page <a href = \"/\">page</a>"

# -----------------------------------------------------------------------------------------------

# Product Insertion Helper Functions
@route ('/insert_product_form_show') # customer reviews etc might not be requried
def insert_product_form_show():


    html = "<style>table, th, td {border: 1px solid black;}</style>"
    html += "<h1> Insertng a Product </h1> <table>"
    html += "<h2> Please use the following Form to Insert a Product</h2>"

    html += product_form_instructions

    html += "<br> Example: ProductID     = UT-12345678"
    html += "<br> Example: Brand         = Marshmello"
    html += "<br> Example: CountryOrigin = Angola"
    html += "<br> Example: CategoryID    = CPA"
    html += "<br> Example: PriceNew      = 120.3"
    html += "<br> Example: PriceUsed     = 110"

    html += "<br> <b>You will be able to search using Brand, CountryOrigin and CategoryID</b>"
    
    html += "<br> <br><a href = \"/all_countries\"> Click here to see Country list </a> <br>"
    html += "<a href = \"/all_categories\"> Click here to see CategoryID List </a> <br>"

    # HTML Form for Inserting Product
    html += '''
    <form action = "/insert_product" method = "post"><br>
      <table>
        <tr><td align="right">ProductID:</td><td align="left"><input type="text" name="ProductID" /></td></tr>
        <tr><td align="right">Brand:</td><td align="left"><input type="text" name="Brand" /></td></tr>
        <tr><td align="right">MaterialColorCapacity:</td><td align="left"><input type="text" name="MaterialColorCapacity"  /></td></tr>
        <tr><td align="right">CountryOrigin:</td><td align="left"><input type="text" name="CountryOrigin"  /></td></tr>
        <tr><td align="right">CustomerReviewsNumber:</td><td align="left"><input type="text" name="CustomerReviewsNumber"  /></td></tr>
        <tr><td align="right">CustomerAverageReview:</td><td align="left"><input type="text" name="CustomerAverageReview"  /></td></tr>
        <tr><td align="right">PriceNew:</td><td align="left"><input type="text" name="PriceNew"  /></td></tr>
        <tr><td align="right">PriceUsed:</td><td align="left"><input type="text" name="PriceUsed"  /></td></tr>
        <tr><td align="right">CategoryID:</td><td align="left"><input type="text" name="CategoryID"  /></td></tr>
      </table>
      <input value = "Insert Product" type = "submit"  />
    </form>
    '''

    return html
    # html = '''
    #     <form action = "/insert_product" method = "post"> <br>
    #         ProductID: <input name = "ProductID" type="text" />  <br>
    #         Brand: <input name = "Brand" type="text" /> <br>
    #         MaterialColorCapacity: <input name = "MaterialColorCapacity" type="text" /> <br>
    #         CountryOrigin: <input name = "CountryOrigin" type="text" /> <br>
    #         CustomerReviewsNumber: <input name = "CustomerReviewsNumber" type="text" /> <br>
    #         CustomerAverageReview: <input name = "CustomerAverageReview" type="text" /> <br>
    #         PriceNew: <input name = "PriceNew" type="text" /> <br>
    #         PriceUsed: <input name = "PriceUsed" type="text" /> <br>
    #         CategoryID: <input name = "CategoryID" type="text" /> <br>
    #         <input value = "Insert!" type = "submit" /> <br>
    #     </form>
    # '''

    # return html

@route ('/insert_product', method ='POST') # implement error handling on conditions
def insert_product():

    ProductID              = request.forms.get("ProductID")
    Brand                  = request.forms.get("Brand")
    MaterialColorCapacity  = request.forms.get("MaterialColorCapacity")
    CountryOrigin          = request.forms.get("CountryOrigin")
    CustomerReviewsNumber  = request.forms.get("CustomerReviewsNumber")
    CustomerAverageReview  = request.forms.get("CustomerAverageReview")
    PriceNew               = request.forms.get("PriceNew")
    PriceUsed              = request.forms.get("PriceUsed")
    CategoryID             = request.forms.get("CategoryID")

    # ## NEED TO CHECK THE NEW PRODUCT TO BE INSERTED
    ret = Product_CHECK(ProductID, False, Brand,\
                   CustomerAverageReview, CustomerReviewsNumber, \
                   CountryOrigin, CategoryID,
                   PriceNew, PriceUsed, False, True)

    if ret != True:
        return ret

    # IF NO ERRORS, EXECUTE:
    cur.execute("insert into Product values (\
        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format\
                                                    (ProductID, \
                                                     Brand, MaterialColorCapacity,\
                                                     CountryOrigin, CustomerReviewsNumber,\
                                                     CustomerAverageReview, PriceNew,\
                                                     PriceUsed, CategoryID))
    con.commit()
    return ProductID +  " has been inserted in the table \
                        </br>  <a href = \"/\">Click here to return to the home-page</a>"

# -----------------------------------------------------------------------------------------------

# Check Sellers (RelationY) related to Product (RelationX) - happens via SellerProductMapping
@route('/sellers_for_product/<ProductID>')
def sellers_for_product(ProductID):
    html = "<style>table, th, td {border: 1px solid black;}</style>"
    html += "<h2> Sellers selling Product with ProductID: {} </h2> <br /> <table>".format(ProductID)

    sql_query = "select * from Seller where SellerID in (select SellerID from SellerProductMapping where ProductID = '{}')".format(ProductID)
    sql_query_output = cur.execute(sql_query)

    html += '''
        <table>
        <th>SellerID</th>
        <th>SellerEmail</th>
        <th>SellerPhone</th>
        <th>SellerAddressStreet</th>
        <th>SellerAddressCity</th>
        <th>SellerAddressState</th>
        <th>SellerAddressZip</th></tr>
    '''

    check_output_size = []

    for row in sql_query_output:
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
            check_output_size.append (str(cell))

    html += "</table><br/><br/><br/>"

    if len(check_output_size) == 0:
        return "Sorry, there are no Sellers yet to be displayed, please add sellers on the previous page."

    html += "Seller can be added using the button below OR using the button in the previous table<br>"

    # Redirect button for adding seller to a product
    html += "<td><a href=\"/insert_seller_for_product_form_show/" + ProductID + "\">Add Seller</a> </td>  </tr>"

    return html

# Update Seller (NOT TO BE IMPLEMENTED)
@route('/update_seller', method = 'POST')
def update_seller():

    # ALL THE NEW / UPDATED TERMS
    SellerID = request.forms.get("SellerID")
    SellerEmail = request.forms.get("SellerEmail")
    SellerPhone = request.forms.get("SellerPhone")
    SellerAddressStreet = request.forms.get("SellerAddressStreet")
    SellerAddressCity = request.forms.get("SellerAddressCity")
    SellerAddressState = request.forms.get("SellerAddressState")
    SellerAddressZip = request.forms.get("SellerAddressZip")

    # Previous / old data is available in lst_seller
    Old_Seller_ID = lst_seller[0]

    SellerID = SellerID if len(SellerID) > 0 else lst_seller[0]
    SellerEmail = SellerEmail if len(SellerEmail) > 0 else lst_seller[1]
    SellerPhone =  SellerPhone if len(SellerPhone) > 0 else lst_seller[2]
    SellerAddressStreet = SellerAddressStreet if len(SellerAddressStreet) > 0 else lst_seller[3]
    SellerAddressCity = SellerAddressCity if len(SellerAddressCity) > 0 else lst_seller[4]
    SellerAddressState = SellerAddressState  if len(SellerAddressState) > 0 else lst_seller[5]
    SellerAddressZip = SellerAddressZip if len(SellerAddressZip) > 0 else lst_seller[6]

    # Update seller details in Seller table (add checks)
    cur.execute("UPDATE Seller SET \
            SellerID = '{}',\
            SellerEmail ='{}', SellerAddressStreet = '{}', SellerAddressCity = '{}', SellerAddressState = '{}',\
            SellerAddressZip = '{}' where SellerID = '{}'".format\
                                                (SellerID, SellerEmail, SellerAddressStreet, SellerAddressCity,\
                                                 SellerAddressState, SellerAddressZip,\
                                                 Old_Seller_ID)) 

    # Update SellerProductMapping as well
    cur.execute("UPDATE SellerProductMapping SET SellerID = '{}' where SellerID = '{}'".format(SellerID, Old_Seller_ID) )

    con.commit()
    return Old_Seller_ID + " Updated </br> return to main <a href = \"/\">page</a>"

# -----------------------------------------------------------------------------------------------

# Add a new seller (relationY) to a product
@route ('/insert_seller_for_product_form_show/<ProductID>') # customer reviews etc might not be requried
def insert_seller_for_product_form_show(ProductID):

    html = "<style>table, th, td {border: 1px solid black;}</style>"
    html = "<h2> Adding a new Seller to ProductID: {} </h2>".format(ProductID)
    html += "<h2> Please use the following Form to Insert a Seller</h2>"

    html += seller_form_instructions
    
    # HTML Form for Inserting Seller
    html += '''
    <form action = "/insert_seller_for_product/{}" method = "post"><br>
      <table>
        <tr><td align="right">SellerID:</td><td align="left"><input type="text" name="SellerID" /></td></tr>
        <tr><td align="right">SellerEmail:</td><td align="left"><input type="email" name="SellerEmail" /></td></tr>
        <tr><td align="right">SellerPhone:</td><td align="left"><input type="text" name="SellerPhone"  /></td></tr>
        <tr><td align="right">SellerAddressStreet:</td><td align="left"><input type="text" name="SellerAddressStreet"  /></td></tr>
        <tr><td align="right">SellerAddressCity:</td><td align="left"><input type="text" name="SellerAddressCity"  /></td></tr>
        <tr><td align="right">SellerAddressState:</td><td align="left"><input type="text" name="SellerAddressState"  /></td></tr>
        <tr><td align="right">SellerAddressZip:</td><td align="left"><input type="text" name="SellerAddressZip"  /></td></tr>
        <tr><td align="right">Inventory:</td><td align="left"><input type="text" name="Inventory"  /></td></tr>

      </table>
      <input value = "Insert Seller" type = "submit"  />
    </form>
    '''.format (ProductID)

    html += "<h2> Please use the following Form to Link an existing Seller to this Product</h2>"
    

    html += "<a href = \"/top_sellers\"> > Click here to see top sellers as examples </a> <br>"
    html += "Inventory should be a natural integer (>=1) and SellerID should be one of those already in the Sellers Table"
    html += "<br> None of them should be empty" 

    # HTML Form for Linking Seller
    html += '''
    <form action = "/link_seller_for_product/{}" method = "post"><br>
      <table>
        <tr><td align="right">SellerID:</td><td align="left"><input type="text" name="SellerID" /></td></tr>
        <tr><td align="right">Inventory:</td><td align="left"><input type="text" name="Inventory" /></td></tr>

      </table>
      <input value = "Link Seller" type = "submit"  />
    </form>
    '''.format (ProductID)


    return html

@route ('/link_seller_for_product/<ProductID>', method='POST')
def link_seller_for_product(ProductID):
    SellerID            = request.forms.get("SellerID")
    Inventory           = request.forms.get("Inventory")

    if len(SellerID) == 0 or len(Inventory) == 0:
        return "None of the fields can be empty!"

    # check sellerID: should be in the Seller table already
    sql_query_output = cur.execute("select SellerID from Seller where SellerID = '{}';".format(SellerID))
    sellercheck = []
    for row in sql_query_output:
        for cell in row:
            # print(str(cell))
            sellercheck.append (str(cell))

    if len(sellercheck) == 0:
        return "This SellerID does not exist"

    # check inventory: should be a whole number
    if not Inventory.isdigit():
        return "Check Inventory Value"
    
    if int(Inventory) < 1:
        return "Check Inventory Value"

    # Create a new mapping for this seller with this product
    cur.execute ("INSERT INTO SellerProductMapping values ('{}', '{}', '{}')".format (SellerID, ProductID, Inventory))

    con.commit()

    html = "<td><a href=\"/sellers_for_product/" + ProductID + "\">See the changes</a> </td>"
    html += ProductID + " has a new seller now! <br>" + SellerID +  " has been linked to it. \
                        </br>  <a href = \"/\">Click here to return to the home-page</a>"


    return html


@route ('/insert_seller_for_product/<ProductID>', method='POST')
def insert_seller_for_product(ProductID):

    # ALL THE NEW / UPDATED TERMS for NEW SELLER (7)
    SellerID            = request.forms.get("SellerID")
    SellerEmail         = request.forms.get("SellerEmail")
    SellerPhone         = request.forms.get("SellerPhone")
    SellerAddressStreet = request.forms.get("SellerAddressStreet")
    SellerAddressCity   = request.forms.get("SellerAddressCity")
    SellerAddressState  = request.forms.get("SellerAddressState")
    SellerAddressZip    = request.forms.get("SellerAddressZip")
    Inventory           = request.forms.get("Inventory")

    # Other checks
    ret = Seller_CHECK (SellerID, SellerEmail, SellerPhone, \
        SellerAddressCity, SellerAddressState, SellerAddressZip, Inventory)
    if ret != True:
        return ret

    # Enter a new seller into the Seller Table
    cur.execute("INSERT INTO Seller values (\
        '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format\
                                                    (SellerID, \
                                                     SellerEmail, SellerPhone,\
                                                     SellerAddressStreet, SellerAddressCity,\
                                                     SellerAddressState, SellerAddressZip))

    # Create a new mapping for this seller with the product we are interested in
    cur.execute ("INSERT INTO SellerProductMapping values ('{}', '{}', '{}')".format (SellerID, ProductID, Inventory))

    con.commit()

    html = "<td><a href=\"/sellers_for_product/" + ProductID + "\">See the changes</a> </td>"
    html += ProductID + " has a new seller now! <br>" + SellerID +  " has been inserted in the table \
                        </br>  <a href = \"/\">Click here to return to the home-page</a>"

    return html

    # return ProductID + " has a new seller now! <br>" + SellerID +  " has been inserted in the table \
    #                     </br>  <a href = \"/\">Click here to return to the home-page</a>"

@route ('/link_seller_product', method='POST')
def link_seller_for_product():
    SellerID            = request.forms.get("SellerID")
    ProductID           = request.forms.get("ProductID")
    Inventory           = request.forms.get("Inventory")

    if len(SellerID) == 0 or len(Inventory) == 0 or len(ProductID) == 0:
        return "None of the fields can be empty!"

    # check sellerID: should be in the Seller table already
    sql_query_output = cur.execute("select SellerID from Seller where SellerID = '{}';".format(SellerID))
    sellercheck = []
    for row in sql_query_output:
        for cell in row:
            # print(str(cell))
            sellercheck.append (str(cell))

    if len(sellercheck) == 0:
        return "This SellerID does not exist"

    # check productID: should be in the Product table already
    sql_query_output = cur.execute("select ProductID from ProductID where ProductID = '{}';".format(ProductID))
    productcheck = []
    for row in sql_query_output:
        for cell in row:
            print(str(cell))
            productcheck.append (str(cell))

    if len(productcheck) == 0:
        return "This ProductID does not exist"

    # check inventory: should be a whole number
    if not Inventory.isdigit():
        return "Check Inventory Value"
    
    if int(Inventory) < 1:
        return "Check Inventory Value"


    # Create a new mapping for this seller with this product
    cur.execute ("INSERT INTO SellerProductMapping values ('{}', '{}', '{}')".format (SellerID, ProductID, Inventory))
    con.commit()

    html = "<td><a href=\"/sellers_for_product/" + ProductID + "\">See the changes</a> </td>"
    html += ProductID + " has a new seller now! <br>" + SellerID +  " has been linked to it. \
                        </br>  <a href = \"/\">Click here to return to the home-page</a>"


    return html


# -----------------------------------------------------------------------------------------------

# Initial Helper functions for searching records (home page)
@route('/all_countries')
def all_countries():
    html = "<h2> Country List </h2> <br /> <table>"

    sql_query = 'select CountryOrigin \
                  from Product group by CountryOrigin'

    for row in cur.execute(sql_query):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"

    html += "</table>"
    html += "<br /><br /><br /><br /><br />"
    return html

@route('/all_brands')
def all_brands():
    html = "<h2> Top 20 Brands List </h2> <br /> <table>"

    # Showing only those brands with >2 sellers
    q = "(select ProductID from SellerProductMapping\
            group by ProductID having count(*) > 2 order by count(*) desc)"

    sql_query = 'select Brand from Product where ProductID in {}\
     order by CustomerAverageReview*CustomerAverageReview limit 30'.format(q)

    for row in cur.execute(sql_query):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"

    html += "</table>"
    html += "<br /><br /><br /><br /><br />"
    return html

@route('/all_categories')
def all_categories():
    html = "<h2> Category List </h2> <br /> <table>"

    sql_query = 'select CategoryID, CategoryName from Category'

    for row in cur.execute(sql_query):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"

    html += "</table>"
    html += "<br /><br /><br /><br /><br />"
    return html

@route('/top_sellers')
def top_sellers():
    html = "<h2> Top Sellers List </h2> <br /> <table>"
    sql_query = 'select SellerID as Number_of_Products\
     from Seller natural join SellerProductMapping group by SellerID order by count(*) desc limit 30'

    for row in cur.execute(sql_query):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"

    html += "</table>"
    html += "<br /><br /><br /><br /><br />"
    return html

@route('/top_products')
def top_products():
    html = "<h2> Top Products List </h2> <br /> <table>"
    sql_query = 'select ProductID\
     from Product natural join SellerProductMapping group by SellerID order by count(*) desc limit 30'

    for row in cur.execute(sql_query):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"

    html += "</table>"
    html += "<br /><br /><br /><br /><br />"
    return html

# -----------------------------------------------------------------------------------------------

# Generic Queries Helper Functions
@route('/top_products_country')
def top_products():
    html = "<h2> Product Average Rating / Country </h2> <br /> <table>"

    sql_query = 'select CountryOrigin, AVG(CustomerAverageReview) as AvgReview \
     			  from Product group by CountryOrigin order by AvgReview desc'# having AvgReview>4.03'

    for row in cur.execute(sql_query):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"

    html += "</table>"
    html += "<br /><br /><br /><br /><br />"
    return html

@route('/top_customers')
def top_customers():
    html = "<h2> Our Top Customers - $100k+ Spent </h2> <br /> <table>"

    sql_query = 'select sum(PriceTotal) as TotalBought, CustomerFirstName, CustomerEmail\
				 from Orders natural join Customer \
				 group by CustomerFirstName\
				 having TotalBought >= 100000\
				 order by TotalBought desc;'

    for row in cur.execute(sql_query):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"

    html += "</table>"
    html += "<br /><br /><br /><br /><br />"
    return html

@route('/wion_day_products')
def wion_day_products():
    html = "<h2> World is One! Day - Product List </h2> <br /> <table>"

    sql_query = 'select ProductID, CountryOrigin from\
				(select *, row_number() over (partition by CountryOrigin\
				order by CustomerAverageReview*CustomerReviewsNumber) \
				as CountryRank from \
				Product left outer join Category using (CategoryID))\
				where CountryRank = 1;'

    for row in cur.execute(sql_query):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"

    html += "</table>"
    html += "<br /><br /><br /><br /><br />"
    return html
# -----------------------------------------------------------------------------------------------

run(host='localhost', port=8080, debug = True)
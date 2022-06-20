import json
from urllib.parse import _ResultMixinBytes
from flask import Flask, abort, request
from about_me import me
from mock_data import catalog
from config import db
from bson import ObjectId

app = Flask("Project")

@app.route("/", methods=['GET'])
def home():
    return "This is the Home page. Welcome World to my little python project."

# create an about endpooint and show your name 

@app.route("/about")
def about():

    return me["first"] + " " + me["last"]
    #return f"{me['first']} {me['last']}"---ALTERNATE WAY TO DISPLAY ARRAY ATTRIBUTES

@app.route("/myaddress")
def address():
    return me["address"]["number"] + " " + me["address"]["street"]
    #  return f'{me["address"]["number"]}  {me["address"]["street"]}' --- alternate way to dispaly array's array's attributes

#################################################################################------ API ENDPOINTS -------#######################################################
# Post man- software used to test endpoints

@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    results = []
    cursor = db.products.find({}) #get all data from collectino/database - curly brakcets used to filter out products.

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)

# POST method to create new produts
@app.route("/api/catalog", methods=["POST"])
def save_product():
    try:
        product = request.get_json()

        # title, at least 5 chars long
        if not "title" in product or len(product["title"]) < 5:
            errors = "Title is required and requires at least 5 characters."

        #must have img
        if not "image" in product or len(product["image"]) < 1:
            errors +=  " Product Image is required."

        # must have price and price be greater than 1
        if not "price" in product or product["price"] < 2:
            errors += " Product must have a minimum cost of 2."

        if errors:
            return abort(400, errors)

        db.products.insert_one(product)
        product["_id"] = str(product["_id"])


        return json.dumps(product)

    except Exception as ex:
        return  abort(500, F"unexpected error: {ex}")


@app.route("/api/catalog/count", methods=["GET"])
def catalog_count():
    # shows counts for how many prodcuts are in the catalog (list/array)
    results = []
    cursor = db.products.find({})

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    counts = len(results)
    return f'There are {json.dumps(counts)} products in our catalog.' #return the value

@app.route("/api/product/<id>", methods=["GET"])
def product_count(id):
    #find the product whos id is equal to ID -in catalog via databse search (find_one)
    try:
        if not ObjectId.is_valid(id):
            return abort(400, "Invalid ID")

        prod = db.products.find_one({"_id": ObjectId(id)})

        if not prod:
            abort(404, "ID does not match any product.")

        prod["_id"] = str([prod["_id"]])
        return json.dumps(prod)
    #raort catching to prevent server crash.
    except:    
        return abort(500, "Unexpected Error.")

    #create a endponit that returns the SUM of all the products prices.
# @app.route("/api/catalog/total", methods=["GET"])-long way to list api route-necessary for api that uses both get and post.
@app.get("/api/catalog/total")
def total_price():

    total = 0 
    cursor = db.products.find({})

    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)

#get api by category
@app.get("/api/section/<category>")
def product_category(category):
    results = []
    cursor = db.products.find({"category": category})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)
    
    return json.dumps(results)

#get the list of categorties
@app.get("/api/categories")
def list_categories():
    cursor = db.products.find({})

    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        if 'Gear' not in results:
            results.append(prod["category"])
        elif 'Weights' not in results:
             results.append(prod["category"])
        #if category does not exist in results, then I will append --done to avoid duplication


    return json.dumps(results)

#get the cheapest product
@app.get("/api/product/cheap/price")
def list_cheap_alt():
    result = []
    for i in catalog:
        result.append(i["price"])
    return json.dumps(min(result))

#alt get the cheapest
@app.get("/api/product/cheap")
def list_cheap():

    cursor = db.products.find({})
    result = cursor[0]
    for i in cursor:
        if i["price"] < result["price"]:
            result = i

    result["_id"] = str(result["_id"])
    return json.dumps(result)

@app.get("/api/exercise1")
def get_exe1():
    nums = [123,123,654,124,8865,532,4768,8476,45762,345,-1,234,0,-12,-456,-123,-865,532,4768]
    solution = {}

    # A: find the lowest number
    solution["a"] = min(nums)


    # B: find how many numbers are lowe than 500
    b = 0
    for i in nums:
        if i < 500:
            b = b + 1
    
    solution["b"] = b

    # C: sum all the negatives ( -xxxxxxxx )
    c = 0
    for i in nums:
        if i < 0:
            c = c + i
    solution["c"] = c


    # D: find the sum of numbers except negatives
    d = 0
    for i in nums:
        if i > 0:
            d = d + i
    solution["d"] = d


    return json.dumps(solution)


########################################
######## Coupon Codes ##################
########################################

#get all
@app.route("/api/coupons/all", methods=["GET"])
def get_all_coupons():
    results = []
    cursor = db.coupons.find({})

    for i in cursor:
        i["_id"] = str(i["_id"])
        results.append(i)


    return json.dumps(results)

#save coupon code
@app.route("/api/coupons", methods=["POST"])
def save_coupon():
    try:
        coupon = request.get_json()

        db.coupons.insert_one(coupon)
        coupon["_id"] = str(coupon["_id"])


        return json.dumps(coupon)

    except:
        return "Save coupon page, error occured"

# get CC by code
@app.route("/api/coupons/<id>", methods=["GET"])
def search_coupon(id):

    coupon = db.coupons.find_one({"_id": ObjectId(id)})
    coupon["_id"] = str(coupon["_id"])


    return json.dumps(coupon)

        
app.run(debug=True)
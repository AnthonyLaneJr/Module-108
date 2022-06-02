import json
from flask import Flask, abort
from about_me import me
from mock_data import catalog

app = Flask("Project")

@app.route("/", methods=['GET'])
def home():
    return "This is the Home page"

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
    return json.dumps(catalog)

@app.route("/api/catalog/count", methods=["GET"])
def catalog_count():
    # shows counts for how many prodcuts are in the catalog (list/array)
    counts = len(catalog)

    return f'There are {json.dumps(counts)} products in our catalog.' #return the value

@app.route("/api/product/<id>", methods=["GET"])
def product_count(id):
    #find the product whos id is equal to ID -in catalog vai traveling catalog with for loop
    for i in catalog:
        if i["_id"] == id:
            return json.dumps(i)
    #return an error if id not correct
    return abort(404, "ID does not match any product.")

    #create a endponit that returns the SUM of all the products prices.
# @app.route("/api/catalog/total", methods=["GET"])-long way to list api route-necessary for api that uses both get and post.
@app.get("/api/catalog/total")
def total_price():

    total = 0 
    for i in catalog:
        total = total + i["price"]

    return json.dumps(total)

#get api by category
@app.get("/api/section/<category>")
def product_category(category):
    results = []
    category = category.lower()
    for i in catalog:
        if i["category"].lower() == category:
            results.append(i)
    
    return json.dumps(results)

#get the list of categorties
@app.get("/api/categories")
def list_categories():
    results = []
    for i in catalog:
        if 'Gear' not in results:
            results.append(i["category"])
        elif 'Weights' not in results:
             results.append(i["category"])
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
    result = catalog[0]
    for i in catalog:
        if i["price"] < result["price"]:
            result = i

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

        
app.run(debug=True)
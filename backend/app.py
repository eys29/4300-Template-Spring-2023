import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import numpy as np
from dotenv import load_dotenv

from db import db
from db import Restaurant, MenuItems

from similarity import get_menu_items_recommendations, edit_distance
from location import get_neighboring_states, get_all_states

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import numpy as np


load_dotenv()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = os.environ.get('MY_PASSWORD')
MYSQL_PORT = 3306
MYSQL_DATABASE = "kardashiandb"

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{mysql_engine.MYSQL_USER}:{mysql_engine.MYSQL_USER_PASSWORD}@{mysql_engine.MYSQL_HOST}:{mysql_engine.MYSQL_PORT}/{mysql_engine.MYSQL_DATABASE}"
db.init_app(app)
with app.app_context():
    db.create_all()
CORS(app)

with app.app_context():
    valid_restaurants = [
        restaurant
        for state in get_all_states()
        for restaurant in Restaurant.query.filter_by(state=state).all() 
    ]
    valid_menu_items = [
        item
        for restaurant in valid_restaurants 
        for item in restaurant.items
    ]
    vectorizer = TfidfVectorizer()
    menu_items_str = [item.str_rep() for item in valid_menu_items]
    tfidf = vectorizer.fit_transform(menu_items_str)
    svd = TruncatedSVD(n_components=40)
    svd_docs = svd.fit_transform(tfidf)
    res = {}
    for i in range(10):
        print('dimension ' + str(i))
        res[i] = []
        sims = cosine_similarity(tfidf, svd.components_[i].reshape(1, -1)).flatten()
        indices = np.argsort(sims)[::-1]
        for j in range(5):
            print(valid_menu_items[indices[j]].rep())
            res[i].append(valid_menu_items[indices[j]].rep())
        
        print()

def test_sim(query, input_item):
    query_vector = vectorizer.transform([query])
    output_item = vectorizer.transform([input_item.str_rep()])
    sims = cosine_similarity(query_vector, svd.components_[:10]).flatten()
    indices = np.argsort(sims)[::-1]
    max_ind = indices[0]
    # print(max_ind)
    # print(res[max_ind])
    output_sim = cosine_similarity(output_item, svd.components_[max_ind].reshape(1, -1)).flatten()
    # print(output_sim)
    
    return res[max_ind], output_sim

# Sample search, the LIKE operator in this case is hard-coded,
# but if you decide to use SQLAlchemy ORM framework,
# there's a much better and cleaner way to do this

@app.route("/")
def home():
    return render_template('base.html', title="sample html")


"""
Takes in query parameters:
location
"""


@app.route("/location")
def location_search():
    location_query = request.args.get("location")
    # states = Restaurant.query.with_entities(Restaurant.state).distinct()
    states = get_all_states()
    results = []
    for state in states:
        edit = edit_distance(location_query, state)
        results.append((edit, state))
    results.sort()
    return success_response({"states": [r[1] for r in results]})


"""
Takes in query parameters:
state
craving
"""


@app.route("/items")
def get_items():
    state = request.args.get("state")
    craving = request.args.get("craving")
    if state is None or craving is None:
        return failure_response("State or Craving not provided!")
    
    similar_items = get_items_from_states(craving, [state])

    #If no similar items found in state, search for items in neighboring states
    if len(similar_items) == 0: 
        region_states = get_neighboring_states(state)
        similar_items = get_items_from_states(craving, region_states)

    # TODO: Use this information    
    for output_item, svd_cossim in similar_items:
        items_most_sim_to_top_eigenvec, eigenvec_cossim = test_sim(craving, output_item[0])
        print(items_most_sim_to_top_eigenvec)
        print(eigenvec_cossim) # probably don't need to use this value, it's not particularly useful
        print(svd_cossim)
        
        

    return success_response({"items": [item.serialize() for (item, rating), csim in similar_items]})

def get_items_from_states(craving, states): 
    valid_restaurants = [
        restaurant
        for state in states
        for restaurant in Restaurant.query.filter_by(state=state).all() 
    ]
    valid_menu_items = [
        (item, restaurant.score) 
        for restaurant in valid_restaurants 
        for item in restaurant.items
    ]
    similar_menu_items = get_menu_items_recommendations(
        craving, valid_menu_items
    )
    return similar_menu_items


"""
"restaurants": {
    "Band W Philly Steaks": {
        "info": {
            "id": 193,
            "position": 23,
            "name": "Band W Philly Steaks",
            "score": "4.7",
            "ratings": "30.0",
            "category": "Salads American Seafood Sandwich Wings",
            "price_range": "$$",
            "full_address": "707 Richard Arrington Junior Boulevard South, 103B, Birmingham, AL, 35233",
            "zip_code": 35233,
            "lat": 33.5083,
            "lng": -86.8004,
            "state": "Alabama"
        },
        "items": [
            {
                "restaurant_id": 193,
                "category": "Gourmet Fries",
                "name": "Ultimate Fries",
                "description": "None",
                "price": "4.99 USD"
            },
            {
                "restaurant_id": 193,
                "category": "Gourmet Fries",
                "name": "Original Fries",
                "description": "None",
                "price": "2.79 USD"
            }
        ]
    },
    "IHOP 2000 Pelham Parkway": {
        "info": {
            "id": 466,
            "position": 12,
            "name": "IHOP 2000 Pelham Parkway",
            "score": "4.6",
            "ratings": "38.0",
            "category": "American Breakfast and Brunch burger Comfort Food Dinner Omelette salad Traditional American Family Meals",
            "price_range": "$",
            "full_address": "2000, Pelham, AL, 35244",
            "zip_code": 35244,
            "lat": 33.344568,
            "lng": -86.7966864,
            "state": "Alabama"
        },
        "items": [
            {
                "restaurant_id": 466,
                "category": "GlutenFriendly",
                "name": "French Fries",
                "description": "GlutenFriendly",
                "price": "3.0 USD"
            }
        ]
    },
    "Dreamland BBQ Birmingham": {
        "info": {
            "id": 221,
            "position": 4,
            "name": "Dreamland BBQ Birmingham",
            "score": "4.5",
            "ratings": "100.0",
            "category": "BBQ Burgers Salads Healthy Family Friendly",
            "price_range": "$",
            "full_address": "1427 14th Ave S, Birmingham, AL, 35205",
            "zip_code": 35205,
            "lat": 33.4939991,
            "lng": -86.802659,
            "state": "Alabama"
        },
        "items": [
            {
                "restaurant_id": 221,
                "category": "FIXINS",
                "name": "FRENCH FRIES",
                "description": "Choose between a small or large basket of french fries",
                "price": "3.49 USD"
            }
        ]
    }, ...
}
"""

@app.route("/items_grouped")
def get_items_grouped():
    state = request.args.get("state")
    craving = request.args.get("craving")
    if state is None or craving is None:
        return failure_response("State or Craving not provided!")

    similar_menu_items = get_items_from_states(craving, [state])

    #If no similar items found in state, search for items in neighboring states
    if len(similar_menu_items) == 0: 
        region_states = get_neighboring_states(state)
        similar_menu_items = get_items_from_states(craving, region_states)

    # valid_restaurants = Restaurant.query.filter_by(state=state).all()
    # valid_menu_items = [
    #     (item, restaurant.score) for restaurant in valid_restaurants for item in restaurant.items]
    # if len(valid_menu_items) == 0:
    #     return success_response({"items": []})
    # similar_menu_items = get_menu_items_recommendations(
    #     craving, valid_menu_items)

    res = {"restaurants":{}}
    for item in similar_menu_items:
        restaurant_name = item.serialize()["restaurant"]["name"]
        if restaurant_name not in res["restaurants"]:
            res["restaurants"][restaurant_name] = {"info": (Restaurant.query.filter_by(id=item.restaurant_id).first()).rep(), "items" : []}
        res["restaurants"][restaurant_name]["items"].append(item.rep())
    return success_response(res)
    
"""
Takes in query parameters:
restaurant id 
"""


@app.route("/restaurant")
def get_restaurant():
    restaurant_id = request.args.get("id")
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    if restaurant is None:
        return failure_response("Restaurant with id", restaurant_id, "not found.")
    return success_response({"restaurant": restaurant.serialize()})



app.run(debug=True)
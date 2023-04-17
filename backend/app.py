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


@app.route("/items_grouped")
def get_items_grouped():
    state = request.args.get("state")
    craving = request.args.get("craving")
    if state is None or craving is None:
        return failure_response("State or Craving not provided!")
    valid_restaurants = Restaurant.query.filter_by(state=state).all()
    valid_menu_items = [
        (item, restaurant.score) for restaurant in valid_restaurants for item in restaurant.item_table]
    if len(valid_menu_items) == 0:
        return success_response({"items": []})
    similar_menu_items = get_menu_items_recommendations(
        craving, valid_menu_items)

    res = {"restaurants":{}}
    for item in similar_menu_items:
        restaurant_name = item.serialize()["restaurant"]["name"]
        if restaurant_name not in res["restaurants"]:
            res["restaurants"][restaurant_name] = []
        res["restaurants"][restaurant_name].append(item.rep())
    return success_response(res)

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
    
    return success_response({"items": [item.serialize() for item in similar_items]})

def get_items_from_states(craving, states): 
    valid_restaurants = [
        restaurant
        for state in states
        for restaurant in Restaurant.query.filter_by(state=state).all() 
    ]
    valid_menu_items = [
        (item, restaurant.score) 
        for restaurant in valid_restaurants 
        for item in restaurant.item_table
    ]
    similar_menu_items = get_menu_items_recommendations(
        craving, valid_menu_items
    )
    return similar_menu_items
    
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


# app.run(debug=True)

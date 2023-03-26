import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import numpy as np
from dotenv import load_dotenv

from db import db
from db import Restaurant, MenuItems

load_dotenv()

def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = os.environ.get('MY_PASSWORD')
MYSQL_PORT = 3306
MYSQL_DATABASE = "4300project"

mysql_engine = MySQLDatabaseHandler(MYSQL_USER,MYSQL_USER_PASSWORD,MYSQL_PORT,MYSQL_DATABASE)

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
def sql_search(episode):
    keys = ["id","title","descr"]
    data = [["a","b","c"]]
    return json.dumps([dict(zip(keys,i)) for i in data])

@app.route("/")
def home():
    return render_template('base.html',title="sample html")

@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)

"""
Takes in query parameters:
location
"""

@app.route("/location")
def location_search():
    def edit_distance(query, message):
        query = query.lower()
        message = message.lower()
        m = len(query) + 1
        n = len(message) + 1
        delete = 1
        insert = 1
        substitute = 2

        edit_matrix = np.zeros((m,n))
        for i in range(1, m): 
            edit_matrix[i][0] = edit_matrix[i-1][0] + delete
        for j in range(1, n): 
            edit_matrix[0][j] = edit_matrix[0][j-1] + insert
        for i in range(1, m):
            for j in range(1, n):
                edit_matrix[i][j] = min(
                    edit_matrix[i-1][j] + delete,
                    edit_matrix[i][j-1] + insert,
                    edit_matrix[i-1][j-1] + (0 if query[i-1] == message[j-1] else substitute)
                )
        return edit_matrix[m-1][n-1]
    location_query = request.args.get("location")
    # indices = [6, 9, 10, 11, 15]
    # column_names = ['name', 'category', 'price_range', 'full_address', 'state']
    # mapping = dict(zip(indices, column_names))
    # query_sql = 
    # data = mysql_engine.query_selector(query_sql)
    # results = set()
    # for l in data:
    #     tmp_dict = {}
    #     for x, value in enumerate(l):
    #         if x in mapping:
    #             tmp_dict[mapping[x]] = value  
    #     edit = edit_distance(location_query, tmp_dict['state'])
    #     results.add((edit, tmp_dict['state']))
    # results = list(results)
    # results.sort()
    # return json.dumps({"results": [i[1] for i in results[:min(10, len(results))]]})

    states = Restaurant.query.with_entities(Restaurant.state).distinct()
    results = []
    for state in states:
        edit = edit_distance(location_query, state['state'])
        if state['state']:
            results.append((edit, state['state']))
    results.sort()
    return success_response({"states": [r[1] for r in results]})




@app.route("/test")
def test_route():
    restaurant = Restaurant.query.filter_by(state='Alabama').first()
    if restaurant is None:
        return failure_response("Restaurant not found!")
    return success_response(
        {"restaurant": restaurant.serialize()}
    )

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
    valid_restaurants = Restaurant.query.filter_by(state=state).all()
    # do cosine similarity math here
    return success_response({"items": [item.serialize() for restaurant in valid_restaurants for item in restaurant.item_table]})

app.run(debug=True)
# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
import os
import pathlib
from flask import session
from flask_bcrypt import Bcrypt

import requests
from flask import Flask, session, abort, redirect, request
from pip._vendor import cachecontrol

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS
bcrypt = Bcrypt(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})  # This will enable CORS for all domains on /api/* routes



# Replace 'your_newsapi_api_key' with your actual News API key

# MongoDB configuration
# You should replace "myDbName" with your actual database name
# and "myUsername:myPassword" with your actual credentials
# "localhost:27017" is the default MongoDB port on your local machine.
# Adjust the URI according to your MongoDB deployment
app.config["MONGO_URI"] = "mongodb+srv://daniyala:KEhA3IsPwwWX6SmF@cluster0.dafwpve.mongodb.net/Test"

mongo = PyMongo(app)    # Initialize PyMongo with the Flask application
# Assuming you're using the mongo.db object to interact with your database
users = mongo.db.users
preferences = mongo.db.preferences


@app.route('/news', methods=['GET'])
def get_news():
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=f8b02b9635ed4db4bae7cad2ee599cd2'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        articles = data['articles']

        filtered_articles = [
            article for article in articles
            if article['urlToImage'] and article['title'].lower() != 'removed'
        ]
        data['articles'] = filtered_articles

        return jsonify(data)
    else:
        return


@app.route('/search')
def search():
    query = request.args.get('query', '')  
    url = (
        'https://newsapi.org/v2/everything?'
        'q={query}&'
        'from=2024-04-11&'
        'sortBy=popularity&'
        'apiKey=f8b02b9635ed4db4bae7cad2ee599cd2'
    ).format(query=query)  # Use string formatting to insert the query

    response = requests.get(url)  # Make the request to the News API
    data = response.json()  # Parse the JSON response

    return jsonify(data)  # Return the JSON response to the client


@app.route('/Login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'email': data['email']})
    if user and check_password(user['password'], data['password']):
        session['user_id'] = str(user['_id'])
        return jsonify({"message": "Logged in successfully."}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)

    #add to mongo db
    mongo.db.users.insert_one({
        "email": data['email'],
        "password": generate_password_hash(data['password']),
        'name' : data['name'],
        'topics': data['topics']
    })
     


    return jsonify(data), 201





@app.route('/picks-for-you', methods=['GET'])
def get_picks(username):
    if 'user_id' not in session:
        return jsonify({"error": "User not authenticated"}), 500
    
    user_preferences = preferences.find_one({'user_id': session['user_id']})
    if user_preferences:
        personalized_content = fetch_content_based_on_preferences(user_preferences)
        return jsonify(personalized_content)
    else:
        return jsonify(fetch_default_content())



@app.route('/category_click', methods=['POST'])
def category_click():
    user_id = request.json.get('user_id')
    category = request.json.get('category')

    # Find the user's document and update the click count for the category
    result = mongo.db.user_clicks.update_one(
        {'user_id': user_id},
        {'$inc': {f'categories.{category}': 1}},
        upsert=True
    )

    if result.modified_count:
        return jsonify({'message': 'Click recorded'}), 200
    else:
        return jsonify({'message': 'Click update failed'}), 500
    




@app.route('/top-stories', methods=['GET'])
def top_stories():
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=f8b02b9635ed4db4bae7cad2ee599cd2'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        articles = data['articles']

        filtered_articles = [
            article for article in articles
            if article['urlToImage'] and article['title'].lower() != 'removed'
        ]
        data['articles'] = filtered_articles

        return jsonify(data)
    else:
        return
 
def check_password(stored_password, provided_password): 
    return bcrypt.check_password_hash(stored_password, provided_password)

def fetch_content_based_on_preferences(user_preferences):
    # Fetch content based on user preferences using API calls
    return []

def fetch_default_content():
    # Fetch default content using API calls
    return []

if __name__ == "__main__":
    app.run(debug=True)

















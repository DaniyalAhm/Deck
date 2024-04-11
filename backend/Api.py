# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})  # This will enable CORS for all domains on /api/* routes

# Replace 'your_newsapi_api_key' with your actual News API key

# MongoDB configuration
# You should replace "myDbName" with your actual database name
# and "myUsername:myPassword" with your actual credentials
# "localhost:27017" is the default MongoDB port on your local machine.
# Adjust the URI according to your MongoDB deployment
app.config["MONGO_URI"] = "mongodb+srv://daniyala:KEhA3IsPwwWX6SmF@cluster0.dafwpve.mongodb.net/Test"



@app.route('/news', methods=['GET'])
def get_news():
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=f8b02b9635ed4db4bae7cad2ee599cd2')
    response = requests.get(url)
    print(response.json())
    if response.status_code == 200:
        return jsonify(response.json())
    
    else:
        return jsonify({"error": "your mom"}), 500
    





@app.route('/search')
def search():
    query = request.args.get('query', '')  # Get the search query from URL parameters

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

if __name__ == '__main__':
    app.run(debug=True)





#making Registration page











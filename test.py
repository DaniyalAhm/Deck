# app.py
from flask import Flask, jsonify
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests



# Initialize the Flask application
app = Flask(__name__)
# Enable CORS
CORS(app)
app = Flask(__name__)

@app.route('/news')
def get_news():
    api_key = 'f8b02b9635ed4db4bae7cad2ee599cd2'
    endpoint = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',  # Specify the country or other parameters
        'apiKey': api_key
    }
    response = requests.get(endpoint, params=params)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)

# app.py

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS
CORS(app)

# Replace 'your_newsapi_api_key' with your actual News API key
NEWS_API_KEY = 'your_newsapi_api_key'

@app.route('/news', methods=['GET'])
def get_news():
    # Get parameters from the query string
    category = request.args.get('category', 'general')
    country = request.args.get('country', 'us')
    pageSize = request.args.get('pageSize', 10)

    # Construct the API request URL
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': country,
        'category': category,
        'pageSize': pageSize,
        'apiKey': NEWS_API_KEY
    }

    # Make the request to the News API
    response = requests.get(url, params=params)

    # Return the response as JSON
    # You might want to handle possible errors here (e.g., invalid API key, network issues)
    return jsonify(response.json())

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
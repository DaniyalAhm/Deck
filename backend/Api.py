# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import os
import pathlib
from flask import session
from flask_bcrypt import Bcrypt
import random
import requests
from flask import Flask, session, abort, redirect, request
from pip._vendor import cachecontrol
from bs4 import BeautifulSoup

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS
bcrypt = Bcrypt(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})  # This will enable CORS for all domains on /api/* routes
import secrets
secret_key = secrets.token_hex(16)
app.secret_key = secret_key


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




    data = response.json()
    Reddit_api = 'FUmo2syXlV5DH88wAteCyf2G9bPBHw'

    reddit_url = 'https://api.reddit.com/r/news/top?limit=100'

    headers = {
        'Authorization': Reddit_api,
        'User-Agent': 'Daniyal'

    }


    response2 = requests.get(reddit_url, headers=headers)
    reddit_data= response2.json()
    if response.status_code == 200:
        data = response.json()
        articles = data['articles']




    for post in reddit_data['data']['children']:
        data['articles'].append({
            'title': post['data']['title']+" -r/News",
            'url': post['data']['url'],
            'urlToImage': get_thumbnail_url(post['data']['url']),
            "description" : get_first_sentences(post['data']['url'])

            
        })

    filtered_articles = [
            article for article in articles
            if article['urlToImage'] and article['title'].lower() != 'removed'
        ]
    data['articles'] = filtered_articles



    return jsonify(data)


@app.route('/search')
def search():
    query = request.args.get('query', '')  
    url = (
        'https://newsapi.org/v2/everything?'
        'q={query}&'
        'from=2024-04-11&'
        'sortBy=popularity&'
        'apiKey=f8b02b9635ed4db4bae7cad2ee599cd2'
    ).format(query=query)  

    response = requests.get(url)  
    data = response.json()  

    return jsonify(data)  


@app.route('/Login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'email': data['email']})
    if user and check_password(user['password'], data['password']):
        session['user_id'] = str(user['_id'])
        return jsonify({"message": "Logged in successfully."}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

#!login with google TO BE DONE


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)

    #add to mongo db
    mongo.db.users.insert_one({
        '_id': generate_unique_id(),
        "email": data['email'],
        "password": register_user(data['password']),
        'name' : data['name'],
        'preferences': data['topics'],
       
    })
     
    return jsonify(data), 201

@app.route('/Business', methods=['GET'])
def Bussiness():
    return jsonify(get_news_by_topics('Business'))

@app.route('/Entertainment', methods=['GET'])
def Entertainment():
    return jsonify(get_news_by_topics('Entertainment'))

@app.route('/Politics', methods=['GET'])
def Politics():
    return jsonify(get_news_by_topics('Politics'))

@app.route('/Health', methods=['GET'])
def Health():
    return jsonify(get_news_by_topics('Health'))

@app.route('/Science', methods=['GET'])
def Science():
    return jsonify(get_news_by_topics('Science'))

@app.route('/Sports', methods=['GET'])
def Sports():
    return jsonify(get_news_by_topics('Sports'))

@app.route('/Technology', methods=['GET'])
def Technology():
    return jsonify(get_news_by_topics('Technology'))





@app.route('/picks-for-you', methods=['GET'])
def get_picks():
    if 'user_id' not in session:
        return jsonify({"error": "User not authenticated"}), 500
    


    user_id = session['user_id']
    user_preferences = mongo.db.users.find_one({'_id': int(user_id)})['preferences']

    print(user_preferences)

    if user_preferences:
        personalized_content = fetch_content_based_on_preferences(user_preferences)
        return jsonify(personalized_content)
    else:
        return jsonify([])




def get_news_by_topics(topics):

    reddit_links ={
        'Business': 'https://api.reddit.com/r/business/top?limit=100',
        'Entertainment': 'https://api.reddit.com/r/entertainment/top?limit=100',
        'General': 'https://api.reddit.com/r/news/top?limit=100',
        'Health': 'https://api.reddit.com/r/health/top?limit=100',
        'Science': 'https://api.reddit.com/r/science/top?limit=100',
        'Sports': 'https://api.reddit.com/r/sports/top?limit=100',
        'Technology': 'https://api.reddit.com/r/technology/top?limit=100',
        'Politics': 'https://api.reddit.com/r/politics/top?limit=100',
    }
    Reddit_api = 'FUmo2syXlV5DH88wAteCyf2G9bPBHw'

    content = []
    headers = {
        'Authorization': Reddit_api,
        'User-Agent': 'Daniyal'
    }
        


    #url for query


    url= 'https://newsapi.org/v2/everything?q='+topics+'&apiKey=f8b02b9635ed4db4bae7cad2ee599cd2'



    response = requests.get(url)




    data = response.json()
    Reddit_api = 'FUmo2syXlV5DH88wAteCyf2G9bPBHw'

    reddit_url = reddit_links[topics]

    headers = {
        'Authorization': Reddit_api,
        'User-Agent': 'Daniyal'

    }


    response2 = requests.get(reddit_url, headers=headers)
    reddit_data= response2.json()
    if response.status_code == 200:
        data = response.json()
        articles = data['articles']




    for post in reddit_data['data']['children']:
        data['articles'].append({
            'title': post['data']['title']+" -r/News",
            'url': post['data']['url'],
            'urlToImage': get_thumbnail_url(post['data']['url']),
            "description" : get_first_sentences(post['data']['url'])

            
        })

    filtered_articles = [
            article for article in articles
            if article['urlToImage'] and article['title'].lower() != 'removed'
        ]
    data['articles'] = filtered_articles

    return data



    

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
            if article['urlToImage'] and article['title'].lower() != 'removed' or None
        ]
        data['articles'] = filtered_articles

        return jsonify(data)
    else:
        return
 


def check_password(stored_password, provided_password): 
    return bcrypt.check_password_hash(stored_password, provided_password)

def register_user( password):
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    # Now store the email and password_hash in your database
    return password_hash

def fetch_content_based_on_preferences(user_preferences):
    # Fetch content based on user preferences using API calls
    list = ['Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology' ]
    reddit_links ={
        'Business': 'https://api.reddit.com/r/business/top?limit=100',
        'Entertainment': 'https://api.reddit.com/r/entertainment/top?limit=100',
        'General': 'https://api.reddit.com/r/news/top?limit=100',
        'Health': 'https://api.reddit.com/r/health/top?limit=100',
        'Science': 'https://api.reddit.com/r/science/top?limit=100',
        'Sports': 'https://api.reddit.com/r/sports/top?limit=100',
        'Technology': 'https://api.reddit.com/r/technology/top?limit=100'
    }
    Reddit_api = 'FUmo2syXlV5DH88wAteCyf2G9bPBHw'

    content = []
    headers = {
        'Authorization': Reddit_api,
        'User-Agent': 'Daniyal'


    }


    
    for topic in list:
        if topic in user_preferences:
            url = reddit_links[topic]
            
            response = requests.get(url, headers=headers)
            reddit_data = response.json()
            for post in reddit_data['data']['children']:
                content.append({
                    'title': post['data']['title']+" (Reddit)",
                    'url': post['data']['url'],
                    'urlToImage': get_thumbnail_url(post['data']['url']),
                    "description" : get_first_sentences(post['data']['url'])

                })



        return jsonify(content)

    #now using news api to search
    api = 'apiKey=f8b02b9635ed4db4bae7cad2ee599cd2'
    q = 'q='
    for topic in list:
        if topic in user_preferences:
            q += topic + ' OR '
    q = q[:-4]
    url = 'https://newsapi.org/v2/everything?'+q+'&'+api
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    for article in articles:
        content.append({
            'title': article['title'],
            'url': article['url'],
            'urlToImage': article['urlToImage']
        })
    
    if(len(content) == 0):
        print("No content found")


    return content


#!Simple webscrapping to get the thumbnail of the article
def get_thumbnail_url(page_url):
    response = requests.get(page_url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
    

    return 'removed'

def generate_unique_id():
    #if the user id is not already in the database
    user_id = random.randint(100000, 999999)
    if mongo.db.users.find_one({'user id': user_id}):
        return generate_unique_id()
    return user_id

import requests
from bs4 import BeautifulSoup

def get_first_sentences(page_url, sentence_count=50):
    response = requests.get(page_url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Attempt to find the main article content
        # Common tags include <article>, <div>, or directly <p> tags within specific containers
        article_body = soup.find('article')
        if not article_body:
            article_body = soup.find('div', {'class': 'post-body'})  # You might need to adjust this class name based on common patterns




        # If an article body container is found, extract text from <p> tags
        if article_body:
            paragraphs = article_body.find_all('p')
            full_text = ' '.join(p.get_text() for p in paragraphs)
            # Split the text into sentences
            sentences = full_text.split(' ')
            # Return the first few sentences
            for i in range(0, len(sentences)):
                if i %5 == 0:
                    sentences[i] = sentences[i] + '\n'

            string =  " ".join(sentences[:sentence_count]) + '.'

         
            return string

    # Return None if no content is found or there's an HTTP error
    return "No Description, Click Read more for more information"


def getRedditnews():
    Reddit_api = 'FUmo2syXlV5DH88wAteCyf2G9bPBHw'

    reddit_url = 'https://api.reddit.com/r/news/top?limit=100'


    reddit_links ={
        'Business': 'https://api.reddit.com/r/business/top?limit=100',
        'Entertainment': 'https://api.reddit.com/r/entertainment/top?limit=100',
        'General': 'https://api.reddit.com/r/news/top?limit=100',
        'Health': 'https://api.reddit.com/r/health/top?limit=100',
        'Science': 'https://api.reddit.com/r/science/top?limit=100',
        'Sports': 'https://api.reddit.com/r/sports/top?limit=100',
        'Technology': 'https://api.reddit.com/r/technology/top?limit=100',
        'Politics': 'https://api.reddit.com/r/politics/top?limit=100',
         'News': reddit_url
    }
    Reddit_api = 'FUmo2syXlV5DH88wAteCyf2G9bPBHw'

    content = []
    headers = {
        'Authorization': Reddit_api,
        'User-Agent': 'Daniyal'


    }

    for topic in list:
            url = reddit_links[topic]
            response = requests.get(url, headers=headers)
            reddit_data = response.json()
            for post in reddit_data['data']['children']:
                content.append({
                    'title': post['data']['title']+" (Reddit)",
                    'url': post['data']['url'],
                    'urlToImage': get_thumbnail_url(post['data']['url'])
                })

    return content


def combine_dataset(data1, data2):
    for post in data2:
        data1['articles'].append({
            'title': post['data']['title']+" (Reddit)",
            'url': post['data']['url'],
            'urlToImage': get_thumbnail_url(post['data']['url'])
        })

    return data1



if __name__ == "__main__":
    app.run(debug=True)

















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
from bson.objectid import ObjectId
import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests



# Initialize the Flask application
app = Flask(__name__)
# Enable CORS
bcrypt = Bcrypt(app)

CORS(app, resources={r"/*": {"origins": "*"}}) 
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

loggedin= False

@app.route('/news', methods=['GET'])
def get_news():
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=f8b02b9635ed4db4bae7cad2ee599cd2'



    response = requests.get(url)




    data = response.json()
    Reddit_api = 'FUmo2syXlV5DH88wAteCyf2G9bPBHw'

    reddit_url = 'https://api.reddit.com/r/news/top?limit=25'

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
    id = generate_unique_id()
    #add to mongo db
    mongo.db.users.insert_one({
        '_id': id,
        "email": data['email'],
        "password": register_user(data['password']),
        'name' : data['name'],
        'selectedTopics': "NONE",
    })

    session.clear()
    session['user_id'] = id
    return jsonify({"message": "User registered successfully"}), 200


     



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
    user_preferences = mongo.db.users.find_one({'_id': (user_id)})['selectedTopics']


    if user_preferences:
        personalized_content = fetch_content_based_on_preferences(user_preferences)
        return jsonify(personalized_content)
    else:
        return jsonify([])



def get_news_by_topics(topics):

    reddit_links ={
        'Business': 'https://api.reddit.com/r/business/top?limit=255',
        'Entertainment': 'https://api.reddit.com/r/entertainment/top?limit=25',
        'General': 'https://api.reddit.com/r/news/top?limit=25',
        'Health': 'https://api.reddit.com/r/health/top?limit=25',
        'Science': 'https://api.reddit.com/r/science/top?limit=25',
        'Sports': 'https://api.reddit.com/r/sports/top?limit=25',
        'Technology': 'https://api.reddit.com/r/technology/top?limit=25',
        'Politics': 'https://api.reddit.com/r/politics/top?limit=25',
    }
    Reddit_api = 'FUmo2syXlV5DH88wAteCyf2G9bPBHw'

    headers = {
        'Authorization': Reddit_api,
        'User-Agent': 'Daniyal'
    }
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
    




def check_password(stored_password, provided_password): 
    return bcrypt.check_password_hash(stored_password, provided_password)

def register_user( password):
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    # Now store the email and password_hash in your database
    return password_hash

def fetch_content_based_on_preferences(user_preferences):
    # Fetch content based on user preferences using API calls
    content = []
    for topic in user_preferences:
        content.append(get_news_by_topics(topic))

    data = content[0]['articles']


    
    for i in range(1, len(content)):

        if 'articles' in content:
            data.extend(content['articles'])

    return (data)


@app.route('/is_active_session' , methods=['GET'])
def is_active_session():
    if 'user_id' in session:
        return jsonify({'active': True}), 200
    else:
        return jsonify({'active': False}), 200




@app.route('/topics', methods=['GET'])
def get_topics():
    return jsonify(['Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'])




@app.route('/update_user_topics', methods=['POST'])
def post():
    data = request.get_json()
    if('user_id' not in session):
        return jsonify({"error": "User not authenticated"}), 500


    user = mongo.db.users.find_one({'_id': session['user_id']})
    filter = {'_id': session['user_id']}
    new_values = {'$set': {'selectedTopics': data['topics']}}

    if user:
        mongo.db.users.update_one(filter=filter, update=new_values)
        return jsonify({"message": "Preferences updated successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404





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
    return str(user_id)



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


@app.route('/getuser_info', methods=['GET'])
def getuser_info():
    if 'user_id' not in session:
        return jsonify({"error": "User not authenticated"}), 500

    print(session['user_id'])
    user = mongo.db.users.find_one({'_id': (session['user_id'])})
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404



@app.route('/update_preferences', methods=['POST'])




def update_preferences():
    data = request.get_json()
    user = mongo.db.users.find_one({'id': session['user_id']})
    if user:
        mongo.db.users.update_one({'email': data['email']}, {'$set': {'preferences': data['preferences']}})
        return jsonify({"message": "Preferences updated successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404





def getRedditnews():
    Reddit_api = 'FUmo2syXlV5DH88wAteCyf2G9bPBHw'

    reddit_url = 'https://api.reddit.com/r/news/top?limit=25'


    reddit_links ={
        'Business': 'https://api.reddit.com/r/business/top?limit=25',
        'Entertainment': 'https://api.reddit.com/r/entertainment/top?limit=25',
        'General': 'https://api.reddit.com/r/news/top?limit=25',
        'Health': 'https://api.reddit.com/r/health/top?limit=25',
        'Science': 'https://api.reddit.com/r/science/top?limit=25',
        'Sports': 'https://api.reddit.com/r/sports/top?limit=25',
        'Technology': 'https://api.reddit.com/r/technology/top?limit=25',
        'Politics': 'https://api.reddit.com/r/politics/top?limit=25',
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




#!#####OAUTH CODE#####


# Ensure you have the correct client secrets path and redirect URI
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "/home/backend/Client_4.json")
GOOGLE_CLIENT_ID = "456548324618-9bjm9d91qjk2grj056sdnass4o7ri8ua.apps.googleusercontent.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Allow unencrypted HTTP for local testing

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

@app.route("/oauth_register", methods=['GET'])
def oauth_register():
    authorization_url, state = flow.authorization_url()
    print(authorization_url, state)
    session["state"] = state
    return redirect(authorization_url)

from google.auth.transport.requests import Request

@app.route("/callback")
def callback():
    if "state" not in session or session["state"] != request.args.get("state"):
        abort(500)  # State does not match

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = requests.session()
    token_request = Request(session=request_session)  # Use Request directly

    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token,  # Ensure to use id_token if available directly
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("email")
    session["name"] = id_info.get("name")

    session['user_id'] = session["google_id"]

    if not mongo.db.users.find_one({'_id': session["google_id"]}):
        #push to mongo db
        mongo.db.users.insert_one({
            '_id': session["google_id"],
            "email": session["google_id"],
            "password": "irc",
            'name' : session["name"],
            'selectedTopics': "NONE",
        })
        return redirect("http://localhost:3001/topics")

    elif mongo.db.users.find_one({'_id': session["google_id"]})  and mongo.db.users.find_one({'_id': session["google_id"]})['selectedTopics'] == "NONE":
        return redirect("http://localhost:3001/topics")

    else:
        return redirect("http://localhost:3001/picks-for-you")
    



if __name__ == "__main__":
    app.run(debug=True)
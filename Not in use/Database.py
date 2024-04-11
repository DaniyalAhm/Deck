from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Database configuration
app.config["MONGO_URI"] = "mongodb+srv://daniyala:KEhA3IsPwwWX6SmF@cluster0.dafwpve.mongodb.net/myDatabase"
mongo = PyMongo(app)

@app.route('/register', methods=['GET'])


def show_register_form():
    # Display the registration form
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    # Hash the password for security
    hashed_password = generate_password_hash(password)
    user_collection = mongo.db.Test  # Ensure 'Test' is the right collection name
    user_collection.insert_one({'name': username, 'password': hashed_password})
    # Redirect to a confirmation page, login page, or somewhere relevant
    return redirect(url_for('login_form'))

@app.route('/login', methods=['GET'])
def login_form():
    # Display the login form
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']
    # Here you would typically verify the username and password against the database
    # Placeholder for actual login logic
    print(f"Username: {username}, Password: {password}")
    # Redirect after login attempt (placeholder URL)
    return redirect('https://one.google.com/storage/management/drive/large?utm_source=gmail&utm_medium=web&utm_campaign=workflow_assist_card_100&g1_landing_page=6')

if __name__ == '__main__':
    app.run(debug=True)

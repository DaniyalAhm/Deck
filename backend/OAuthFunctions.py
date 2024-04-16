import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask("Google Login App")
app.secret_key = "0234485734895734897523"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "456548324618-ctjl1to88i49b8gc5f63gpf65bh0tvmf.apps.googleusercontent.com" # You might need to use your own ID from Cloud Console I'm not sure
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

#This function might need modification before the site being published
#It is a label so that not all routes are accessible prior to login
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

### Check this function to see how user info gets passed to the next route
@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("email") #this might be the thing to push to Mongo, or maybe email instead
    session["name"] = id_info.get("name")
    return redirect("/select_preferences")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return "<a href='/login'><button>Login</button></a>"


@app.route("/select_preferences")
@login_is_required
def select_preferences():
    return f"Hello {session['google_id']}! <br/> <a href='/logout'><button>Logout</button></a>" # I can update this test HTML to actually select the preferences


if __name__ == "__main__":
    app.run(debug=True)
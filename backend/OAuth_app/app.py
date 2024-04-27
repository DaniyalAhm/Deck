from flask import Flask, redirect, request, session, abort
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
import os
import pathlib
import requests
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

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
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    if "state" not in session or session["state"] != request.args.get("state"):
        abort(500)  # State does not match

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = google.auth.transport.requests.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("email")
    session["name"] = id_info.get("name")

    return redirect("/welcome")

@app.route("/welcome")
def welcome():
    if "name" in session:
        return f"Welcome, {session['name']}!"
    return "User not logged in"

if __name__ == "__main__":
    app.run(debug=True, port=5000)

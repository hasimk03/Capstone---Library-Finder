import os
import pathlib
from flask import Blueprint, Response, render_template, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests

views = Blueprint('views', __name__)

#creating different pages

GOOGLE_CLIENT_ID = "105638364377-m4meho7lb50kgbc1urrmtihvgtnfcip6.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def login_required(function):
        def wrapper(*args, **kwargs):
            
            if 'google_id' not in session:
                return abort(401)
            else:
                return function()
        wrapper.__name__ = function.__name__
        return wrapper




@views.route("/")
def home():
    return render_template("home.html")

@views.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@views.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/home")

@views.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@views.route('/home')
@login_required
def import_home():
    return render_template("home_logged_in.html")

@views.route('/Livingston')
@login_required
def import_livi():
    return render_template("room.html")

@views.route('/Busch')
@login_required
def import_busch():
    return "<h1>Busch</h1>"

@views.route('/Busch/Room1')
@login_required
def import_busch1():
    return render_template('room.html')

@views.route('/CollegeAve')
@login_required
def import_collegeave():
    return "<h1>CollegeAve</h1>"

@views.route('/CookDoug')
@login_required
def import_cookdoug():
    return "<h1>CookDoug</h1>"

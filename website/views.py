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

def calculate_ticks(percentage):
    ticks = 440*(1-percentage)
    return ticks

def calc_percentage(current, occupancy = 10):
    percentage = current/occupancy
    return percentage

def get_current():
    file = open("Download.txt", 'r')
    txt = file.readlines()
    last = txt[-1]
    seg = last.split("|")
    return int((seg[1]))

def get_date():
    file = open("Download.txt", 'r')
    txt = file.readlines()
    last = txt[-1]
    seg = last.split("|")
    return int((seg[2]))

def get_time():
    file = open("Download.txt", 'r')
    txt = file.readlines()
    last = txt[-1]
    seg = last.split("|")
    return int((seg[3]))

def display_percentage(current, occupancy = 10):
    percentage = current/occupancy
    return(f"{percentage:.0%}")


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
    name = session.get('name')
    return render_template("home_logged_in.html",name = name)

# Busch-->LSM---->1st Floor
@views.route('/Busch/LSM/1st_Floor')
@login_required
def import_busch_lsm_1st_floor():
    return render_template('room.html', room="LSM 1st Floor", percentage="75%", ticks=calculate_ticks(.75))

# Busch-->LSM---->2nd Floor
@views.route('/Busch/LSM/2nd_Floor')
@login_required
def import_busch_lsm_2nd_floor():
    return render_template('room.html', room="LSM 2nd Floor", percentage="75%", ticks=calculate_ticks(.75))

# Busch-->LSM---->3rd Floor
@views.route('/Busch/LSM/3rd_Floor')
@login_required
def import_busch_lsm_3rd_floor():
    return render_template('room.html', room="LSM 3rd Floor", percentage="75%", ticks=calculate_ticks(.75))


# Busch-->Student_Center---->The_Cove
@views.route('/Busch/student_center/the_cove')
@login_required
def import_busch_studentCenter_the_cove():
    return render_template('room.html', room="The Cove", percentage="75%", ticks=calculate_ticks(.75))

# Busch-->Student_Center---->International_Lounge
@views.route('/Busch/student_center/international_lounge')
@login_required
def import_busch_studentCenter_international_lounge():
    return render_template('room.html', room="International Lounge", percentage="75%", ticks=calculate_ticks(.75))


# Busch-->Student_Center---->Quiet_Study_Room
@views.route('/Busch/student_center/quiet_study_room')
@login_required
def import_busch_studentCenter_quiet_study_room():
    return render_template('room.html', room="quiet_study_room", percentage="75%", ticks=calculate_ticks(.75))


# Livingston-->Kilmer_Library---->Basement
@views.route('/Livingston/kilmer_library/basement')
@login_required
def import_livingston_kilmer_library_basement():
    return render_template('room.html', room="Basement", percentage="75%", ticks=calculate_ticks(.75))

# Livingston-->Kilmer_Library---->1st Floor
@views.route('/Livingston/kilmer_library/1st_floor')
@login_required
def import_livingston_kilmer_library_1st_floor():
    return render_template('room.html', room="1st Floor", percentage="75%", ticks=calculate_ticks(.75))

# Livingston-->Kilmer_Library---->2nd Floor
@views.route('/Livingston/kilmer_library/2nd_floor')
@login_required
def import_livingston_kilmer_library_2nd_floor():
    return render_template('room.html', room="2nd Floor", percentage="75%", ticks=calculate_ticks(.75))

# Livingston-->Student_Center---->The Space
@views.route('/Livingston/student_center/the_space')
@login_required
def import_livingston_student_center_the_space():
    return render_template('room.html', room="The Space", percentage="75%", ticks=calculate_ticks(.75))

# Livingston-->Student_Center---->1st Floor Lounge
@views.route('/Livingston/student_center/1st_floor_lounge')
@login_required
def import_livingston_student_center_1st_floor_lounge():
    return render_template('room.html', room="1st Floor Lounge", percentage="75%", ticks=calculate_ticks(.75))

# Livingston-->Student_Center---->Coffe_House
@views.route('/Livingston/student_center/coffe_house')
@login_required
def import_livingston_student_center_coffe_house():
    return render_template('room.html', room="Coffee House", percentage="75%", ticks=calculate_ticks(.75))

# Douglass-->Student_Center---->Douglass_Lounge
@views.route('/Douglass/student_center/douglass_lounge')
@login_required
def import_douglass_student_center_douglass_lounge():
    return render_template('room.html', room="Douglass Lounge", percentage="75%", ticks=calculate_ticks(.75))

# Douglass-->Student_Center---->Quiet Study Room
@views.route('/Douglass/student_center/quiet_study_room')
@login_required
def import_douglass_student_center_quiet_study_room():
    return render_template('room.html', room="Quiet Study Room", percentage="75%", ticks=calculate_ticks(.75))

# Douglass-->Student_Center---->NJC Lounge
@views.route('/Douglass/student_center/njc_lounge')
@login_required
def import_douglass_student_center_njc_lounge():
    return render_template('room.html', room="NJC Lounge", percentage="75%", ticks=calculate_ticks(.75))

# Cook-->Student_Center---->2nd Floor Lounge
@views.route('/Cook/student_center/2nd_floor_lounge')
@login_required
def import_cook_student_center_2nd_floor_lounge():
    return render_template('room.html', room="2nd Floor Lounge", percentage="75%", ticks=calculate_ticks(.75))

# Cook-->Student_Center---->2nd Floor Quiet Lounge
@views.route('/Cook/student_center/2nd_floor_quiet_lounge')
@login_required
def import_cook_student_center_2nd_floor_quiet_lounge():
    return render_template('room.html', room="2nd Floor Quiet Lounge", percentage="75%", ticks=calculate_ticks(.75))

# Mabel Smith Library -->Student_Center---->1st Floor Lounge
@views.route('/mabel_swith_library/student_center/1st_floor_lounge')
@login_required
def import_mabel_swith_library_student_center_1st_floor_lounge():
    return render_template('room.html', room="1st Floor Lounge", percentage="75%", ticks=calculate_ticks(.75))

# Mabel Smith Library -->Student_Center---->2nd Floor Lounge
@views.route('/mabel_swith_library/student_center/2nd_floor_lounge')
@login_required
def import_mabelswithLibrary_student_center_2nd_floor_lounge():
    return render_template('room.html', room="2nd Floor Lounge", percentage="75%", ticks=calculate_ticks(.75))

# College Ave-->Alexander Library---->1st Floor Commons Area
@views.route('/College_Ave/alexander_library/1st_floor_commons_area')
@login_required
def import_College_Ave_alexander_library_1st_floor_commons_area():
    return render_template('room.html', room="1st Floor Commons Area", percentage="75%", ticks=calculate_ticks(.75))

# College Ave-->Alexander Library---->2nd Floor
@views.route('/College_Ave/alexander_library/2nd_floor')
@login_required
def import_College_Ave_alexander_library_2nd_floor():
    return render_template('room.html', room="2nd Floor", percentage="75%", ticks=calculate_ticks(.75))

# College Ave-->Alexander Library---->3rd Floor
@views.route('/College_Ave/alexander_library/3rd_floor')
@login_required
def import_College_Ave_alexander_library_3rd_floor():
    return render_template('room.html', room="3rd Floor", percentage="75%", ticks=calculate_ticks(.75))

# College Ave-->Student Center--->Main Lounge
@views.route('/College_Ave/student_center/main_lounge')
@login_required
def import_College_Ave_student_center_main_lounge():
    return render_template('room.html', room="Main Lounge", percentage="75%", ticks=calculate_ticks(.75))

# College Ave-->Student Center--->Red Lion Cafe
@views.route('/College_Ave/student_center/red_Lion_cafe')
@login_required
def import_College_Ave_student_center_red_lion_cafe():
    return render_template('room.html', room="Red Lion Cafe", percentage="75%", ticks=calculate_ticks(.75))

# College Ave-->Student Center--->4th Floor Lounge
@views.route('/College_Ave/student_center/4th_floor_lounge')
@login_required
def import_College_Ave_student_center_4th_floor_lounge():
    return render_template('room.html', room="4th Floor Lounge", percentage="75%", ticks=calculate_ticks(.75))

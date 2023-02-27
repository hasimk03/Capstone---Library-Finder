from flask import Blueprint, render_template

views = Blueprint('views', __name__)

#creating different pages
@views.route("/")
def home():
    return render_template("home.html")


@views.route('/Livingston')
def import_livi():
    return "<h1>Livi</h1>"

@views.route('/Busch')
def import_busch():
    return "<h1>Busch</h1>"

@views.route('/CollegeAve')
def import_collegeave():
    return "<h1>CollegeAve</h1>"

@views.route('/CookDoug')
def import_cookdoug():
    return "<h1>CookDoug</h1>"
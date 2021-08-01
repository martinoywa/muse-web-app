from flask import Blueprint


home = Blueprint("home", __name__)
@home.route("/")
def index():
    return "Home Page"


login = Blueprint("login", __name__)
@login.route("/login")
def user_login():
    return "Log In Page"


signup = Blueprint("signup", __name__)
@signup.route("/signup")
def user_signup():
    return "Sign Up Page"


details = Blueprint("details", __name__)  # song details
@details.route("/details/id")
def song_details(id):
    return "Details Page"


list = Blueprint("list", __name__)  # list per quadrant
@list.route("/list/id")
def quadrant_list(id):
    return "List Page"


upload = Blueprint("upload", __name__)
@upload.route("/upload")
def song_upload():
    return "Upload Page"

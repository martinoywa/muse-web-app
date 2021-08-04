from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from app import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        # user actually exists?
        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("auth.login"))
        else:
            login_user(user, remember=remember)
            return redirect(url_for("main.playlist"))
    # if request.method == "GET":
    return render_template("login.html")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()    # if this returns a user then user exists

        if user:    # try again
            flash("Email address already exists")
            return redirect(url_for("auth.signup"))

        new_user = User(email=email, name=name, password=generate_password_hash(password,
                                                                                method="sha256"))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))
    return render_template("signup.html")

@auth.route("/signout")
@login_required
def signout():
    logout_user()
    return render_template("index.html")

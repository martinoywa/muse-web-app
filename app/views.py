from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Songs
from app import db


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")

 
@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)

@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        title = request.form.get("title")
        name = request.form.get("name")
        album = request.form.get("album")
        lyrics = request.form.get("lyrics")
        song_file = request.form.get("song")

        print(type(song_file))
        print(song_file)

        song = Songs.query.filter_by(title=title).first()

        if song:
            flash("Song by already exists")
            return redirect(url_for("main.upload"))

        new_song = Songs(title=title, name=name, album=album, lyrics=lyrics)

        db.session.add(new_song)
        db.session.commit()

        return redirect(url_for("main.profile"))
    return render_template("upload.html")

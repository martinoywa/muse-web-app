from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Track
from app import db

from random import randint

random_quadrant = randint(1, 4)


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")

 
@main.route("/playlist")
@login_required
def playlist():
    list_q1 = Track.query.filter_by(quadrant=1)
    list_q2 = Track.query.filter_by(quadrant=2)
    list_q3 = Track.query.filter_by(quadrant=3)
    list_q4 = Track.query.filter_by(quadrant=4)

    return render_template("playlist.html", list_q1=list_q1, list_q2=list_q2,
                           list_q3=list_q3, list_q4=list_q4)

@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        title = request.form.get("title")
        name = request.form.get("name")
        album = request.form.get("album")
        lyrics = request.form.get("lyrics")
        song_file = request.form.get("song")
        quadrant = random_quadrant

        song = Track.query.filter_by(title=title).first()

        if song:
            flash("Song by already exists")
            return redirect(url_for("main.upload"))

        new_song = Track(quadrant=quadrant, title=title, name=name, album=album,
                         lyrics=lyrics)

        db.session.add(new_song)
        db.session.commit()

        return redirect(url_for("main.playlist"))
    return render_template("upload.html")

@main.route("/track/<int:track_id>", methods=["GET"])
@login_required
def track(track_id):
    track = Track.query.filter_by(id=track_id).first()
    return render_template("track.html", track=track)

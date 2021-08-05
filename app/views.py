from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Track
from app import db

from .spectrogram import create_spectrogram
from .model.inference import aggregate_inference

from pathlib import Path


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
        song_file = request.files["song"]

        song = Track.query.filter_by(title=title).first()
        artist = Track.query.filter_by(name=name).first()

        if song and artist:
            flash("Song by already exists")
            return redirect(url_for("main.upload"))

        # create spectrogram and get quadrant
        create_spectrogram(song_file)
        spectrogram = Path("app/static/spectrogram/file.png")
        quadrant = aggregate_inference(spectrogram, lyrics)

        if quadrant:
            new_song = Track(quadrant=quadrant, title=title, name=name, album=album,
                             lyrics=lyrics)
            db.session.add(new_song)
            db.session.commit()
        else:
            flash("Failed to process cluster")
            return redirect(url_for("main.upload"))

        return redirect(url_for("main.playlist"))
    return render_template("upload.html")

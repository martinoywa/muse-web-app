from pathlib import Path

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from .model.inference import aggregate_inference
from .models import Track
from .spectrogram import create_mel_spectrogram

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/clusters")
@login_required
def clusters():
    list_q1 = Track.query.filter_by(quadrant=1)
    list_q2 = Track.query.filter_by(quadrant=2)
    list_q3 = Track.query.filter_by(quadrant=3)
    list_q4 = Track.query.filter_by(quadrant=4)

    return render_template("clusters.html", list_q1=list_q1, list_q2=list_q2,
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
        create_mel_spectrogram(song_file)
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

        return redirect(url_for("main.clusters"))
    return render_template("upload.html")


@main.route("/track/<int:track_id>", methods=["GET"])
@login_required
def track(track_id):
    track = Track.query.filter_by(id=track_id).first()
    return render_template("track.html", track=track)

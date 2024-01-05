from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from flask_login import current_user, login_required
from . import *
from .models import Active_Users, Winners

scenes = Blueprint('scenes', __name__)


@scenes.route('/scene', methods=["GET", "POST"])
@login_required
def scene():
    Username = current_user.Username
    User = Active_Users.query.filter_by(Username = Username).first()
    if request.method == "POST":
        if "Next" in request.form:
            User.Progress += 1
            db.session.commit()
        elif "Prev" in request.form:
            User.Progress -= 1
            db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("Scene.html", Progress = User.Progress, Username = Username, Lives=User.Lives)

@scenes.route('/Failed', methods=["GET", "POST"])
@login_required
def endgame():
    Username = current_user.Username
    User = Active_Users.query.filter_by(Username = Username).first()
    Lives = User.Lives
    if request.method == "POST":
        return redirect(url_for('auth.Logout'))
    return render_template("GameOver.html", Username = Username, Lives = Lives)

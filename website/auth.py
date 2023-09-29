from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, login_user, current_user, logout_user
from .models import Active_Users, Winners
from . import *

auth = Blueprint('auth', __name__)

@auth.route('/Login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        if request.method == "POST":
            Username = request.form.get("Username")

            user1 = Winners.query.filter_by(Username=Username).first()
            user2 = Active_Users.query.filter_by(Username=Username).first()
            if user1 or user2:
                flash("Username has been Taken!", category="error")
            elif len(Username)<3:
                flash("Username Too Short!!", category="error")
            else:
                New_User = Active_Users(Username = Username)
                db.session.add(New_User)
                db.session.commit()
                login_user(New_User, remember=True)
                return redirect(url_for('views.home'))
    return render_template("Login.html")

@auth.route('/Logout')
@login_required
def Logout():
    Username = current_user.Username
    User = Active_Users.query.filter_by(Username = Username).first()
    db.session.delete(User)
    db.session.commit()
    logout_user()
    return redirect(url_for('home.start'))
from flask import redirect, Blueprint, request, url_for, render_template
from flask_login import current_user

home = Blueprint('home', __name__)

@home.route('/', methods=['GET','POST'])
def start():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == "POST":
        return redirect(url_for('auth.Login'))
    return render_template('Home.html')
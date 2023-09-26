from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import Active_Users, Winners
from . import *
from .Puzzles import Puzzle1, Puzzle2, Puzzle3, Puzzle4
views = Blueprint('views', __name__)

#Puzzle 1 variables
global Guesses,Result
Result = "Null"
#Puzzle 1 variables

@views.route('/home', methods=["POST", "GET"])
@login_required
def home():
    Lives = Active_Users.query.filter_by(Username = current_user.Username).first().Lives
    if Lives > 0:
        Alive = "True"
    else:
        Alive = "False"
    Progress = Active_Users.query.filter_by(Username = current_user.Username).first().Progress
    if request.method == "POST":
        if 'Puz1' in request.form:
            return redirect(url_for('views.Puz1'))
        elif 'Puz2' in request.form:
            return redirect(url_for('views.Puz2'))
        elif 'Puz3' in request.form:
            return redirect(url_for('views.Puz3'))
        elif 'Puz4' in request.form:
            return redirect(url_for('views.Puz4'))
        elif 'Retry' in request.form:
            user = Active_Users.query.get(Username = current_user.Username).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                flash('You can use the Same Username and go Again!', category="success")
                return redirect(url_for('auth.Logout'))
            else:
                flash('Nothing is happening cause User Not Found!', category="error")
    return render_template("Base.html", Username = current_user.Username, Progress = Progress, Alive = Alive)

@views.route('/Puz1', methods=["POST", "GET"])
@login_required
def Puz1():
    
    global Guesses, Result
    Result = "Null"
    Guesses = []
    # Initialize wordle_data from the session if it exists
    Username = current_user.Username
    User = Active_Users.query.filter_by(Username=Username).first()
    if User.Progress != 0:
        return redirect(url_for('views.home'))
    wordle_data = session.get(f'wordle_data {Username}', {
        'guesses': [],
        'word': Puzzle1.generate_random_word().upper(),
        'feedback': "",
        'guess_result': [],
        'result': "Null"
    })

    if request.method == "POST":
        if "Submit" in request.form:
            return redirect(url_for('views.home'))
        elif "Try" in request.form:
            User.Attempts -= 1
            db.session.commit()
            Guess = request.form.get("Guess")
            Guess = Guess.upper()
            if len(Guess) < 5 or len(Guess) > 5 or not Guess.isalpha() or not Puzzle1.is_valid_word(Guess):
                flash("Incorrect Input Type or Not a Valid Word", category="error")
                User.Attempts += 1
                db.session.commit()
            else:
                wordle_data['feedback'] = Puzzle1.play_wordle(wordle_data['word'], Guess)
                wordle_data['guess_result'] = [(i, j) for i, j in zip(Guess, wordle_data['feedback'])]

                # Append the new guess result to the existing guesses data
                wordle_data['guesses'].append(wordle_data['guess_result'])

                if wordle_data['word'] == Guess:
                    Result = "Success"
                    user = Active_Users.query.filter_by(Username=Username).first()
                    if user:
                        user.Progress = user.Progress + 1
                        user.Attempts = 5
                        db.session.commit()
                    session.pop(f'wordle_data {Username}')
                    

            Guesses = wordle_data['guesses']
            session[f'wordle_data {Username}'] = wordle_data
    elif "Back" in request.form:
        return redirect(url_for('views.Puz1'))
    if User.Attempts == 0 and wordle_data['result']=="Null":
        words = wordle_data['word']
        flash(f"Failure! The Word was {words}", category="error")
        Result = "Failed"
        user = Active_Users.query.filter_by(Username=Username).first()
        if user:
            user.Lives -= 1
            user.Attempts = 5
            db.session.commit()
        session.pop(f'wordle_data {Username}')
        return render_template("Puz1.html", Username=Username, Guesses=Guesses, Result=Result)
    return render_template("Puz1.html", Username=Username, Guesses=Guesses, Result=Result)

@views.route('/Puz2', methods=["POST", "GET"])
@login_required
def Puz2():
    global Guesses, Result
    Guesses = []
    Result = "Null"
    Username = current_user.Username
    User = Active_Users.query.filter_by(Username=Username).first()
    if User.Progress != 1:
        return redirect(url_for('views.home'))
    user_data = session.get(f'numpat_data {Username}')

    if user_data is None:
        # Generate the puzzle if it hasn't been generated yet
        user_data = {
            'series': Puzzle2.generate_modified_series(),
        }
        session[f'numpat_data {Username}'] = user_data
    ans = user_data['series'][5]
    if request.method == "POST":
        if "Submit" in request.form:
            return redirect(url_for('views.home'))
        elif "Try" in request.form:
            User.Attempts -= 1
            db.session.commit()
            Guesss = request.form.get("Guess")
            if len(Guesss)<1 or not Guesss.isdigit():
                flash('Wrong Input Format!', category="error")
                User.Attempts += 1
                db.session.commit()
            else:
                Guess = int(Guesss)
                ans = user_data['series'][5]
                
                if Guess == ans:
                    Result = "Success"
                    user = Active_Users.query.filter_by(Username=Username).first()
                    if user:
                        user.Progress = user.Progress + 1
                        user.Attempts = 5
                        db.session.commit()
                    session.pop(f'numpat_data {Username}')
        elif "Retry" in request.form:
            return redirect(url_for('views.Puz2')) 
            
    Guesses = user_data['series'][:5]
    if User.Attempts == 0 and Result=="Null":
        flash(f"Failure! The Number was {ans}", category="error")
        Result = "Failed"
        user = Active_Users.query.filter_by(Username=Username).first()
        if user:
            user.Lives -= 1
            user.Attempts = 5
            db.session.commit()
        session.pop(f'numpat_data {Username}')
        return render_template("Puz2.html", Username=Username, Guesses=Guesses, Result=Result, attempts = User.Attempts)
    return render_template("Puz2.html", Username = Username,nums = Guesses, Result = Result, attempts=User.Attempts)

@views.route('/Puz3', methods=["POST", "GET"])
@login_required
def Puz3():
    global Guesses, Result
    Result = "Null"
    Username = current_user.Username
    User = Active_Users.query.filter_by(Username=Username).first()
    if User.Progress != 2:
        return redirect(url_for('views.home'))
    usr_data = session.get(f'mgcsqr_data {Username}')

    if usr_data is None:
        # Generate the puzzle if it hasn't been generated yet
        usr_data = {
            'series': Puzzle3.generate_magic_square()
        }
        session[f'mgcsqr_data {Username}'] = usr_data
    Guesses = usr_data['series']
    if request.method == "POST":
        if "Submit" in request.form:
            user = Active_Users.query.filter_by(Username = Username).first()
            if user:
                user.Progress = user.Progress + 1
                user.Attempts = 5
                db.session.commit()

                return redirect(url_for('views.home'))
        
        elif "Try" in request.form:
            User.Attempts-=1
            db.session.commit()
            Guess = []
            names = "textbox_"
            for i in range(3):
                row = []
                for j in range(3):
                    try:
                        val = int(request.form.get(f'{names}{i}{j}'))
                        row.append(val)
                    except ValueError:
                        flash(f'Input not valid', category="error")
                        User.Attempts += 1
                        db.session.commit()
                        return render_template("Puz3.html", Username = Username,Num = Guesses, Result = Result)
                        
                Guess+=row
            if Puzzle3.check_invalid(Guesses[0], Guess):
                flash('Input not in specified manner!', category="error")
                User.Attempts += 1
                db.session.commit()
                return render_template("Puz3.html", Username = Username,Num = Guesses, Result = Result)
            else:
                ans = usr_data['series'][1]
                if Puzzle3.check_magic_sq([Guess,ans]):
                    Result = "Success"
                    User.Attempts = 5
                    db.session.commit()
                    session.pop(f'mgcsqr_data {Username}')

        elif "Retry" in request.form:
            return redirect(url_for("views.Puz3"))
    if User.Attempts == 0 and Result=="Null":
        flash(f"Failure!", category="error")
        Result = "Failed"
        user = Active_Users.query.filter_by(Username=Username).first()
        if user:
            user.Lives -= 1
            user.Attempts = 5
            db.session.commit()
        session.pop(f'mgcsqr_data {Username}')
        return render_template("Puz3.html", Username=Username, Num=Guesses, Result=Result, attempts = User.Attempts)    
    return render_template("Puz3.html", Username = Username,Num = Guesses, Result = Result, Attempts = User.Attempts)

@views.route('/Puz4', methods=["POST", "GET"])
@login_required
def Puz4():
    global Guesses, Result
    Result = "Null"
    Username = current_user.Username
    usr_data = session.get(f'anagram_data {Username}')
    User = Active_Users.query.filter_by(Username=Username).first()
    if User.Progress != 3:
        return redirect(url_for('views.home'))
    if usr_data is None:
        # Generate the puzzle if it hasn't been generated yet
        usr_data = {
            'puzzle': Puzzle4.Anagram_Puzzle()
        }
        session[f'anagram_data {Username}'] = usr_data
    Guesses = usr_data['puzzle']
    Word = Guesses[0]
    Hint = Guesses[1]
    if request.method == "POST":
        if "Submit" in request.form:
            user = Active_Users.query.filter_by(Username = Username).first()
            if user:
                user.Progress = user.Progress + 1
                user.Attempts = 5
                db.session.commit()

                return redirect(url_for('views.home'))
        elif "Try" in request.form:
            User.Attempts -=  1
            db.session.commit()
            Guess = request.form.get("Guess")
            if Guess.lower() == Guesses[1].lower():
                Result = "Success"
                User.Attempts = 5
                db.session.commit()
                session.pop(f'anagram_data {Username}')
            else:
                flash('Wrong Answer HEHE!', category="error")
        elif "Retry" in request.form:
            return redirect(url_for('views.Puz4'))
    if User.Attempts == 0 and Result=="Null":
        flash(f"Failure! The Word was {Hint}", category="error")
        Result = "Failed"
        user = Active_Users.query.filter_by(Username=Username).first()
        if user:
            user.Lives -= 1
            user.Attempts = 5
            db.session.commit()
        session.pop(f'anagram_data {Username}')
        return render_template("Puz4.html", Username=Username, Word=Word, Result=Result,Hint = Hint, attempts = User.Attempts)
    return render_template("Puz4.html", Username = Username, Word = Word, Result = Result, Hint = Hint, attempts = User.Attempts)

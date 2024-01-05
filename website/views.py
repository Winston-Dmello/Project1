from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import Active_Users, Winners
from sqlalchemy.sql import func, text, cast
from sqlalchemy.types import Float
from . import *
from datetime import datetime, timedelta
from .Puzzles import Puzzle1, Puzzle2, Puzzle3, Puzzle4, MinSec
views = Blueprint('views', __name__)

#Puzzle 1 variables
global Guesses,Result
Result = "Null"
#Puzzle 1 variables

@views.route('/home', methods=["POST", "GET"])
@login_required
def home():
    session.clear()
    Username = current_user.Username
    User = Active_Users.query.filter_by(Username = Username).first()
    if User.Lives != 0:
        if User.Progress in [0, 1, 3, 4, 6, 7, 9, 10, 12, 13]:
            return redirect(url_for('scenes.scene'))
        elif User.Progress == 2:
            return redirect(url_for('views.Puz1'))
        elif User.Progress == 5:
            return redirect(url_for('views.Puz2'))
        elif User.Progress == 8:
            return redirect(url_for('views.Puz3'))
        elif User.Progress == 11:
            return redirect(url_for('views.Puz4'))
        elif User.Progress == 14:
            return redirect(url_for('views.Victory'))
    else:
        return redirect(url_for('scenes.endgame'))
    return render_template("Base.html", Username = current_user.Username, Progress = User.Progress, Lives=User.Lives)

@views.route('/Puz1', methods=["POST", "GET"])
@login_required
def Puz1():
    
    global Guesses, Result
    Result = "Null"
    Guesses = []
    # Initialize wordle_data from the session if it exists
    Username = current_user.Username
    User = Active_Users.query.filter_by(Username=Username).first()
    if User.Progress != 2:
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
        if user.Lives == 0:
            return redirect(url_for('views.home'))
    return render_template("Puz1.html", Username=Username, Guesses=Guesses, Result=Result, Lives=User.Lives)

@views.route('/Puz2', methods=["POST", "GET"])
@login_required
def Puz2():
    global Guesses, Result
    Guesses = []
    Result = "Null"
    Username = current_user.Username
    User = Active_Users.query.filter_by(Username=Username).first()
    if User.Progress != 5:
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
        if user.Lives == 0:
            return redirect(url_for('views.home'))
    return render_template("Puz2.html", Username = Username,nums = Guesses, Result = Result, attempts=User.Attempts, Lives=User.Lives)

@views.route('/Puz3', methods=["POST", "GET"])
@login_required
def Puz3():
    global Guesses, Result
    Result = "Null"
    Username = current_user.Username
    User = Active_Users.query.filter_by(Username=Username).first()
    if User.Progress != 8:
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
                        return render_template("Puz3.html", Username = Username,Num = Guesses, Result = Result, Lives=User.Lives)
                        
                Guess+=row
            if Puzzle3.check_invalid(Guesses[0], Guess):
                flash('Input not in specified manner!', category="error")
                User.Attempts += 1
                db.session.commit()
                return render_template("Puz3.html", Username = Username,Num = Guesses, Result = Result, Lives=User.Lives)
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
        if user.Lives == 0:
            return redirect(url_for('views.home'))    
    return render_template("Puz3.html", Username = Username,Num = Guesses, Result = Result, Attempts = User.Attempts, Lives=User.Lives)

@views.route('/Puz4', methods=["POST", "GET"])
@login_required
def Puz4():
    global Guesses, Result
    Result = "Null"
    Username = current_user.Username
    usr_data = session.get(f'anagram_data {Username}')
    User = Active_Users.query.filter_by(Username=Username).first()
    if User.Progress != 11:
        return redirect(url_for('views.home'))
    if usr_data is None:
        # Generate the puzzle if it hasn't been generated yet
        usr_data = {
            'puzzle': Puzzle4.Anagram_Puzzle()
        }
        session[f'anagram_data {Username}'] = usr_data
    Guesses = usr_data['puzzle']
    Word = Guesses[0]
    Hint = Guesses[2]
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
        if user.Lives == 0:
            return redirect(url_for('views.home'))
    return render_template("Puz4.html", Username = Username, Word = Word, Result = Result, Hint = Hint, attempts = User.Attempts, Lives=User.Lives)

@views.route('/Victory', methods=["POST", "GET"])
@login_required
def Victory():
    Username = current_user.Username
    Winner = Winners.query.filter_by(Username=Username).first()
    User = Active_Users.query.filter_by(Username=Username).first()
    if User.Progress != 14:
        return redirect(url_for('views.home'))
    if not Winner:

        time_taken_expr = func.strftime('%s', func.now()) - func.strftime('%s', User.Start_Time)
        

        Winner = Winners(
            Username=User.Username,
            Time_Taken=time_taken_expr
        )
        db.session.add(Winner)
        db.session.commit()
        Winner = Winners.query.filter_by(Username = Username).first()
        Winner.Time_Taken = MinSec.Calcu(Winner.Time_Taken)
        db.session.commit()
        
    top_winners = Winners.query.order_by(Winners.Time_Taken.asc())
    index = 0
    for record in top_winners:
        index += 1
        if record.Username == Username:
            break
    user_rank = index

    # Get the top 10 winners
    top_10_winners = top_winners.limit(10).all()

    if request.method == "POST":
        db.session.delete(User)
        db.session.commit()
        return redirect(url_for('auth.Logout'))

    return render_template("Victory.html", Winner=Winner, Rank=user_rank, TopWinners=top_10_winners)
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully",category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Try Again", category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign-up", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 5 characters", category='error')
        elif len(firstName) < 2:
            flash("First Name must be greater than 3 characters", category='error')
        elif password != confirmPassword:
            flash("Password don't match", category='error')
        elif len(password) < 7:
            flash("Password is too short", category='error')
        else:
            new_user = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()          
            login_user(user, remember=True)
            flash("Account Created", category='success')
            return redirect(url_for('views.home'))
            

    return render_template('sign_up.html', user=current_user)




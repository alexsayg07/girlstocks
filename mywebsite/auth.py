from flask import Blueprint, render_template, flash, url_for, redirect, request
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, current_user, login_required
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return (redirect(url_for('views.mystocks')))
            else:
                flash('Incorrect password, try again.', category='error')
        else: 
            flash('Email does not exist.')
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/signup",  methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # TODO: Check validity of signup
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be valid', category='error')
        elif len(first_name) <2:
            flash('First name is too short', category='error')
        elif password1!=password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Pass word must be at least 7 characters', category= 'error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()

            flash('Account created!', category= 'success')
            login_user(user, remember=True)

            return(redirect(url_for('views.mystocks')))


    return render_template("signup.html", user=current_user)


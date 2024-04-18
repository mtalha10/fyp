from flask import Blueprint, render_template, request, flash, redirect, url_for  # Importing Flask components
from .models import User  # Importing the User model
from werkzeug.security import generate_password_hash, check_password_hash  # Importing password hashing functions
from . import db  # Importing the db instance from __init__.py
from flask_login import login_user, login_required, logout_user, current_user  # Importing functions for user authentication

auth = Blueprint('auth', __name__)  # Creating a Blueprint for authentication routes

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Checking if the request method is POST
        email = request.form.get('email')  # Getting the email from the form
        password = request.form.get('password')  # Getting the password from the form

        user = User.query.filter_by(email=email).first()  # Querying the User table for a user with the provided email
        if user:  # If a user with the provided email exists
            if check_password_hash(user.password, password):  # Checking if the password is correct
                flash('Logged in successfully!', category='success')  # Flashing a success message
                login_user(user, remember=True)  # Logging in the user
                return redirect(url_for('views.home'))  # Redirecting to the home page
            else:
                flash('Incorrect password, try again.', category='error')  # Flashing an error message for incorrect password
        else:
            flash('Email does not exist.', category='error')  # Flashing an error message for non-existing email

    return render_template("login.html", user=current_user)  # Rendering the login template with the current user

@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Logging out the current user
    return redirect(url_for('auth.login'))  # Redirecting to the login page

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':  # Checking if the request method is POST
        email = request.form.get('email')  # Getting the email from the form
        first_name = request.form.get('firstName')  # Getting the first name from the form
        password1 = request.form.get('password1')  # Getting the first password from the form
        password2 = request.form.get('password2')  # Getting the second password from the form

        user = User.query.filter_by(email=email).first()  # Querying the User table for a user with the provided email
        if user:  # If a user with the provided email already exists
            flash('Email already exists.', category='error')  # Flashing an error message
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')  # Flashing an error message for short email
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')  # Flashing an error message for short first name
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')  # Flashing an error message for mismatched passwords
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')  # Flashing an error message for short password
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))  # Creating a new user with hashed password
            db.session.add(new_user)  # Adding the new user to the database session
            db.session.commit()  # Committing the changes to the database
            login_user(new_user, remember=True)  # Logging in the new user
            flash('Account created!', category='success')  # Flashing a success message
            return redirect(url_for('views.home'))  # Redirecting to the home page

    return render_template("sign_up.html", user=current_user)  # Rendering the sign-up template with the current user

from flask import Blueprint, render_template, request, flash, jsonify  # Importing Flask components
from flask_login import login_required, current_user  # Importing functions for user authentication
from .models import Note  # Importing the Note model
from . import db  # Importing the db instance from __init__.py
import json  # Importing JSON module

views = Blueprint('views', __name__)  # Creating a Blueprint for views routes

@views.route('/', methods=['GET', 'POST'])
@login_required  # Requiring login to access this route
def home():
    if request.method == 'POST':  # Checking if the request method is POST
        note = request.form.get('note')  # Getting the note from the form

        if len(note) < 1:  # Checking if the note is empty
            flash('Note is too short!', category='error')  # Flashing an error message
        else:
            new_note = Note(data=note, user_id=current_user.id)  # Creating a new note
            db.session.add(new_note)  # Adding the new note to the database session
            db.session.commit()  # Committing the changes to the database
            flash('Note added!', category='success')  # Flashing a success message

    return render_template("home.html", user=current_user)  # Rendering the home template with the current user

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # Parsing the JSON data from the request
    noteId = note['noteId']  # Getting the ID of the note to be deleted
    note = Note.query.get(noteId)  # Querying the Note table for the note with the specified ID
    if note:  # If the note exists
        if note.user_id == current_user.id:  # If the note belongs to the current user
            db.session.delete(note)  # Deleting the note from the database session
            db.session.commit()  # Committing the changes to the database

    return jsonify({})  # Returning an empty JSON response



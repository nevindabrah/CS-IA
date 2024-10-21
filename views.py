from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Image
from . import db
import json
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Add code here to handle POST request
        pass
    return render_template("home.html", user=current_user)

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/to-do', methods=['GET'])
@login_required
def todo():
    return render_template("to-do.html", user=current_user)

@views.route('/timetable', methods=['GET', 'POST'])
@login_required
def timetable():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        file = request.files['file']
        title = request.form.get('title')  # Capture the title from the form
        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            mimetype = file.mimetype
            img = Image(img=file.read(), name=filename, mimetype=mimetype, user_id=current_user.id, title=title)
            db.session.add(img)
            db.session.commit()
            flash('Image uploaded successfully!', category='success')
            return redirect(url_for('views.timetable'))
    images = Image.query.filter_by(user_id=current_user.id).all()
    return render_template("timetable.html", user=current_user, images=images)

@views.route('/delete-image/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get(image_id)
    if image and image.user_id == current_user.id:
        db.session.delete(image)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

@views.route('/edit-image/<int:image_id>', methods=['POST'])
@login_required
def edit_image(image_id):
    image = Image.query.get(image_id)
    if image and image.user_id == current_user.id:
        title = request.form.get('title')
        file = request.files.get('file')
        if title:
            image.title = title
        if file:
            image.img = file.read()
            image.name = secure_filename(file.filename)
            image.mimetype = file.mimetype
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})
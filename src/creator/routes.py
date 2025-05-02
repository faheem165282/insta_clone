from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import uuid
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from src import db
from src.creator import bp
# Defining form class directly to avoid import issues
from src.models import Photo

# Define the form class directly here to avoid import errors
class UploadPhotoForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    caption = TextAreaField('Caption', validators=[Length(max=200)])
    location = StringField('Location', validators=[Length(max=100)])
    people = StringField('People in Photo', validators=[Length(max=200)])
    submit = SubmitField('Upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'creator':
        flash('Access denied. You need to be a creator to view this page.')
        return redirect(url_for('main.index'))
    
    photos = Photo.query.filter_by(user_id=current_user.id).order_by(Photo.upload_date.desc()).all()
    return render_template('creator/dashboard.html', title='Creator Dashboard', photos=photos)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.role != 'creator':
        flash('Access denied. You need to be a creator to upload photos.')
        return redirect(url_for('main.index'))
    
    form = UploadPhotoForm()
    if form.validate_on_submit():
        if form.photo.data and allowed_file(form.photo.data.filename):
            # Generate a unique filename to avoid collisions
            filename = secure_filename(form.photo.data.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # Save file to local storage
            photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            form.photo.data.save(photo_path)
            
            # Save metadata to database
            photo = Photo(
                title=form.title.data,
                caption=form.caption.data,
                location=form.location.data,
                people=form.people.data,
                filename=unique_filename,
                user_id=current_user.id
            )
            db.session.add(photo)
            db.session.commit()
            
            flash('Your photo has been uploaded!')
            return redirect(url_for('creator.dashboard'))
        else:
            flash('Invalid file format. Please upload a PNG, JPG, JPEG, or GIF file.')
    
    return render_template('creator/upload.html', title='Upload Photo', form=form)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_photo(id):
    if current_user.role != 'creator':
        flash('Access denied. You need to be a creator to delete photos.')
        return redirect(url_for('main.index'))
    
    photo = Photo.query.get_or_404(id)
    if photo.user_id != current_user.id:
        flash('You can only delete your own photos.')
        return redirect(url_for('creator.dashboard'))
    
    # Delete the physical file
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filename))
    except:
        # File might be already gone, continue with database deletion
        pass
    
    # Delete from database
    db.session.delete(photo)
    db.session.commit()
    flash('Your photo has been deleted.')
    return redirect(url_for('creator.dashboard'))

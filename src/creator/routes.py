from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import uuid
from src import db
from src.creator import bp
from src.creator.forms import UploadMediaForm
from src.models import Photo

# Maximum file sizes
MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB

# Allowed file extensions
ALLOWED_PHOTO_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi'}

def allowed_file(filename, media_type):
    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if media_type == 'photo':
        return extension in ALLOWED_PHOTO_EXTENSIONS
    elif media_type == 'video':
        return extension in ALLOWED_VIDEO_EXTENSIONS
    return False

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
        flash('Access denied. You need to be a creator to upload media.')
        return redirect(url_for('main.index'))
    
    form = UploadMediaForm()
    
    if form.validate_on_submit():
        file = form.media_file.data
        media_type = form.media_type.data
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer to the beginning
        
        # Validate file size
        if (media_type == 'photo' and file_size > MAX_PHOTO_SIZE) or \
           (media_type == 'video' and file_size > MAX_VIDEO_SIZE):
            max_size_mb = MAX_PHOTO_SIZE / (1024 * 1024) if media_type == 'photo' else MAX_VIDEO_SIZE / (1024 * 1024)
            flash(f'{media_type.capitalize()} size exceeds maximum limit of {max_size_mb}MB!')
            return redirect(url_for('creator.upload'))
        
        # Validate file extension
        if not allowed_file(file.filename, media_type):
            allowed_extensions = ALLOWED_PHOTO_EXTENSIONS if media_type == 'photo' else ALLOWED_VIDEO_EXTENSIONS
            flash(f'Invalid file extension. Allowed extensions for {media_type}: {", ".join(allowed_extensions)}')
            return redirect(url_for('creator.upload'))
        
        # Secure the filename and make it unique
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Save the file
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
        
        # Create a database record
        photo = Photo(
            title=form.title.data,
            caption=form.caption.data,
            location=form.location.data,
            people=form.people.data,
            filename=unique_filename,
            media_type=media_type,
            file_size=file_size,
            user_id=current_user.id
        )
        db.session.add(photo)
        db.session.commit()
        
        flash(f'Your {media_type} has been uploaded!')
        return redirect(url_for('creator.dashboard'))
    
    return render_template('creator/upload.html', title='Upload Media', form=form)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.role != 'creator':
        flash('Access denied. You need to be a creator to delete media.')
        return redirect(url_for('main.index'))
    
    photo = Photo.query.get_or_404(id)
    
    # Check if the logged-in user is the owner of the photo
    if photo.user_id != current_user.id:
        flash('Access denied. You can only delete your own media.')
        return redirect(url_for('creator.dashboard'))
    
    # Delete the file from the filesystem
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filename))
    except Exception as e:
        flash(f'Error deleting file: {str(e)}')
    
    # Delete the database record and related comments/likes
    db.session.delete(photo)
    db.session.commit()
    
    flash('Media deleted successfully!')
    return redirect(url_for('creator.dashboard'))

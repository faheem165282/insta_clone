from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from src import db
from src.consumer import bp
from src.models import Photo, Comment, Like
from src.consumer.forms import CommentForm, SearchForm

# Explicitly define the gallery route with the correct decorator
@bp.route('/gallery')
@login_required
def gallery():
    search_form = SearchForm()
    query = request.args.get('query', '')
    
    if query:
        # Basic search functionality
        photos = Photo.query.filter(
            (Photo.title.contains(query)) | 
            (Photo.caption.contains(query)) | 
            (Photo.location.contains(query)) | 
            (Photo.people.contains(query))
        ).order_by(Photo.upload_date.desc()).all()
    else:
        photos = Photo.query.order_by(Photo.upload_date.desc()).all()
    
    return render_template('consumer/gallery.html', title='Photo Gallery', 
                          photos=photos, search_form=search_form)

@bp.route('/photo/<int:id>', methods=['GET', 'POST'])
@login_required
def photo_detail(id):
    photo = Photo.query.get_or_404(id)
    comment_form = CommentForm()
    
    # Handle comment submission
    if comment_form.validate_on_submit():
        comment = Comment(
            content=comment_form.content.data,
            user_id=current_user.id,
            photo_id=photo.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!')
        return redirect(url_for('consumer.photo_detail', id=photo.id))
    
    # Get existing comments
    comments = Comment.query.filter_by(photo_id=photo.id).order_by(Comment.created_at.desc()).all()
    
    # Check if current user has already liked this photo
    user_like = Like.query.filter_by(user_id=current_user.id, photo_id=photo.id).first()
    
    # Count total likes
    likes_count = Like.query.filter_by(photo_id=photo.id).count()
    
    return render_template('consumer/photo_detail.html', title=photo.title, 
                          photo=photo, comment_form=comment_form, comments=comments,
                          user_like=user_like, likes_count=likes_count)

@bp.route('/like/<int:id>', methods=['POST'])
@login_required
def like_photo(id):
    photo = Photo.query.get_or_404(id)
    
    # Check if user already liked this photo
    existing_like = Like.query.filter_by(user_id=current_user.id, photo_id=photo.id).first()
    
    if existing_like:
        # User already liked this photo, so unlike it
        db.session.delete(existing_like)
        db.session.commit()
        liked = False
    else:
        # User hasn't liked this photo yet, so add a like
        new_like = Like(
            user_id=current_user.id,
            photo_id=photo.id
        )
        db.session.add(new_like)
        db.session.commit()
        liked = True
    
    # Count total likes
    likes_count = Like.query.filter_by(photo_id=photo.id).count()
    
    return jsonify({'success': True, 'liked': liked, 'likesCount': likes_count})

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from src import db
from src.consumer import bp
from src.models import Photo, Comment, Rating
from src.consumer.forms import CommentForm, SearchForm

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
    
    # Get existing comments and ratings
    comments = Comment.query.filter_by(photo_id=photo.id).order_by(Comment.created_at.desc()).all()
    
    # Check if current user has already rated this photo
    user_rating = Rating.query.filter_by(user_id=current_user.id, photo_id=photo.id).first()
    
    # Calculate average rating
    ratings = Rating.query.filter_by(photo_id=photo.id).all()
    avg_rating = sum([r.rating for r in ratings]) / len(ratings) if ratings else 0
    
    return render_template('consumer/photo_detail.html', title=photo.title, 
                          photo=photo, comment_form=comment_form, comments=comments,
                          user_rating=user_rating, avg_rating=avg_rating)

@bp.route('/rate/<int:id>/<int:rating>', methods=['POST'])
@login_required
def rate_photo(id, rating):
    if not 1 <= rating <= 5:
        return jsonify({'success': False, 'message': 'Invalid rating value'})
    
    photo = Photo.query.get_or_404(id)
    
    # Check if user already rated this photo
    existing_rating = Rating.query.filter_by(user_id=current_user.id, photo_id=photo.id).first()
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating
        db.session.commit()
    else:
        # Create new rating
        new_rating = Rating(
            rating=rating,
            user_id=current_user.id,
            photo_id=photo.id
        )
        db.session.add(new_rating)
        db.session.commit()
    
    # Recalculate average rating
    ratings = Rating.query.filter_by(photo_id=photo.id).all()
    avg_rating = sum([r.rating for r in ratings]) / len(ratings) if ratings else 0
    
    return jsonify({'success': True, 'avgRating': avg_rating})

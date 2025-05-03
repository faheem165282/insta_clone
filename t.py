from src import create_app, db
from src.models import Photo

app = create_app()

with app.app_context():
    # Update all existing records to have default values
    photos = Photo.query.all()
    for photo in photos:
        photo.media_type = 'photo'  # Set default type for existing photos
        photo.file_size = 0  # Set a default file size since we don't know the actual sizes
    db.session.commit()
    print(f"Updated {len(photos)} existing photos")

exit()
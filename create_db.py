from src import create_app, db
from src.models import User, Photo, Comment, Rating

app = create_app()
app.app_context().push()

# Create database tables
db.create_all()

print("Database tables created successfully!")

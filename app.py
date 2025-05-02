from src import create_app, db
from src.models import User, Photo, Comment, Rating

# Create the Flask application instance
# This needs to be a global variable named 'app' for Azure App Service
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Photo': Photo, 'Comment': Comment, 'Rating': Rating}

# This block only runs when executing the file directly, not when imported
if __name__ == '__main__':
    app.run()

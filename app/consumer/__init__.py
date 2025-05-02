from flask import Blueprint

bp = Blueprint('consumer', __name__)

from app.consumer import routes

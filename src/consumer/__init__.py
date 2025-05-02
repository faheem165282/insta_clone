from flask import Blueprint

bp = Blueprint('consumer', __name__)

from src.consumer import routes

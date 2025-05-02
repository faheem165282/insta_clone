from flask import Blueprint

bp = Blueprint('creator', __name__)

from src.creator import routes

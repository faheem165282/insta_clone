from flask import render_template, redirect, url_for
from src.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

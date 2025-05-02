from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class UploadPhotoForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    caption = TextAreaField('Caption', validators=[Length(max=200)])
    location = StringField('Location', validators=[Length(max=100)])
    people = StringField('People in Photo', validators=[Length(max=200)])
    submit = SubmitField('Upload')

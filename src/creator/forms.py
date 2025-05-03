from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class UploadMediaForm(FlaskForm):
    media_type = SelectField('Media Type', choices=[('photo', 'Photo'), ('video', 'Video')], validators=[DataRequired()])
    media_file = FileField('Media File', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'], 'Images and videos only!')
    ])
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    caption = TextAreaField('Caption', validators=[Length(max=200)])
    location = StringField('Location', validators=[Length(max=100)])
    people = StringField('People', validators=[Length(max=200)])
    submit = SubmitField('Upload')

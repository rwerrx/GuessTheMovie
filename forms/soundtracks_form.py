from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, RadioField
from wtforms.validators import DataRequired


class SoundtrackAnswerForm(FlaskForm):
    answer1 = RadioField(choices=[])
    answer2 = RadioField(choices=[])
    answer3 = RadioField(choices=[])
    answer4 = RadioField(choices=[])
    answer5 = RadioField(choices=[])
    submit = SubmitField('Ответить')

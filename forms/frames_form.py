from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, RadioField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    answer2 = RadioField(choices=[])
    answer3 = RadioField(choices=[])

    submit = SubmitField('Ответить')

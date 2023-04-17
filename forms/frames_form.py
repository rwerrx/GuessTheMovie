from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, RadioField
from wtforms.validators import DataRequired, InputRequired


class FramesAnswerForm(FlaskForm):
    answer1 = RadioField(choices=[], default=1, validators=[DataRequired("123123")])
    answer2 = RadioField(choices=[], default=1, validators=[DataRequired()])
    answer3 = RadioField(choices=[], default=1, validators=[DataRequired()])
    answer4 = RadioField(choices=[], default=1, validators=[DataRequired()])
    answer5 = RadioField(choices=[], default=1, validators=[DataRequired()])

    submit = SubmitField('Ответить')

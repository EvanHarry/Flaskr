from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired(), Length(1, 64), ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

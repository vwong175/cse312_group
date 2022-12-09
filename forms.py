from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="A username is required"), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(message="A proper email is required"), Email()])

    password = PasswordField('Password', validators=[DataRequired(message="A password is required")])

    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])

    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="A proper email is required"), Email()])

    password = PasswordField('Password', validators=[DataRequired(message="A password is required")])

    remember = BooleanField('Remember me')

    submit = SubmitField('Login')

class JoinRoom(FlaskForm):
    roomID = StringField('RoomID', validators=[DataRequired(message="A room id is required")])
    submit = SubmitField('Join Room')

class editUserForm(FlaskForm):
    newUsername = StringField('New Username', validators=[DataRequired(message="A username is required"), Length(min=2, max=20)])
    submit = SubmitField('Edit Username')

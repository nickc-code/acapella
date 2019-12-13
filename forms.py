from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from server.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username',
		validators=[DataRequired(), Length(min=2, max=20)])
	email= StringField('Email',
		validators=[DataRequired(), Email()])
	password= PasswordField('Password', validators=[DataRequired()])
	confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit=SubmitField('Sign Up')

	def validate_username(self, username):
		user=User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken please choose a different one')

	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken please choose a different one')

class LoginForm(FlaskForm):
	email= StringField('Email',
		validators=[DataRequired(), Email()])
	password= PasswordField('Password', validators=[DataRequired()])
	remember=BooleanField('Remember me')
	submit=SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username',
		validators=[DataRequired(), Length(min=2, max=20)])
	email= StringField('Email',
		validators=[DataRequired(), Email()])
	picture= FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit=SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user=User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken please choose a different one')

	def validate_email(self, email):
		if email.data != current_user.email:
			user=User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken please choose a different one')

class PostForm(FlaskForm):
	title=StringField('Title', validators=[DataRequired()])
	content=TextAreaField('Content', validators=[DataRequired()])
	content2=StringField('Assign To', validators=[DataRequired()])
	submit=SubmitField('Assign')

class ExerciseForm(FlaskForm):
	title=StringField('title', validators=[DataRequired()])
	date_due=StringField('date_due', validators=[DataRequired()])
	description=StringField('description', validators=[DataRequired()])
	link=StringField('link', validators=[DataRequired()])
	submit=SubmitField('submit')

class TempoForm(FlaskForm):
	title=StringField('title', validators=[DataRequired()])
	date_due=StringField('date_due', validators=[DataRequired()])
	description=StringField('description', validators=[DataRequired()])
	link=StringField('link', validators=[DataRequired()])
	submit=SubmitField('submit')

class PitchForm(FlaskForm):
	title=StringField('title', validators=[DataRequired()])
	date_due=StringField('date_due', validators=[DataRequired()])
	description=StringField('description', validators=[DataRequired()])
	link=StringField('link', validators=[DataRequired()])
	submit=SubmitField('submit')
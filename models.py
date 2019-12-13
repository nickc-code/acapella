from datetime import datetime
from server import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(20), unique=True, nullable=False)
	email=db.Column(db.String(120), unique=True, nullable=False)
	image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
	password=db.Column(db.String(60), nullable=False)
	post = db.relationship('Post', backref='author', lazy=True)
	exercise = db.relationship('Exercise', backref='author', lazy=True)
	tempo = db.relationship('Tempo', backref='author', lazy=True)
	pitch = db.relationship('Pitch', backref='author', lazy=True)


	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(100), nullable=False)
	date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content=db.Column(db.Text, nullable=False)
	content2=db.Column(db.Text, nullable=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"

class Exercise(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(100), nullable=False)
	date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	date_due=db.Column(db.String(100), nullable=False)
	description=db.Column(db.Text, nullable=False)
	link=db.Column(db.Text, nullable=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Exercise('{self.title}', '{self.date_posted}','{self.date_due}', '{self.description}', '{self.link}')"


class Tempo(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(100), nullable=False)
	date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	date_due=db.Column(db.String(100), nullable=False)
	description=db.Column(db.Text, nullable=False)
	link=db.Column(db.Text, nullable=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Tempo('{self.title}', '{self.date_posted}','{self.date_due}', '{self.description}', '{self.link}')"

class Pitch(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(100), nullable=False)
	date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	date_due=db.Column(db.String(100), nullable=False)
	description=db.Column(db.Text, nullable=False)
	link=db.Column(db.Text, nullable=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Pitch('{self.title}', '{self.date_posted}','{self.date_due}', '{self.description}', '{self.link}')"



if __name__ == '__main__':
	db.create_all()
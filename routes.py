from flask import redirect, request
from server import app, db, bcrypt
from flask import render_template, url_for, flash, abort
from server.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ExerciseForm, TempoForm, PitchForm
from server.models import User, Post, Exercise, Tempo, Pitch
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify

@app.route('/')
def Home():
	return render_template('Home.html')

@app.route('/SingerHome')
@login_required
def SingerHome():
	posts = Post.query.all()
	return render_template('SingerHome.html', posts=posts)

@app.route('/UserHome', methods=['GET', 'POST'])
@login_required
def UserHome():
	posts = Post.query.all()
	# posts = Post.query.filter_by(author=author)
	return render_template('UserHome.html', posts=posts)




current_id_2 = 4
counts = {}
sales = [
	# {
	# 	"id": 1,
	# 	"Assigned By": "Casey",
	# 	"Member": "Julia",
	# 	"Task": "Learn notes for Rolling Stone"
	# },
	# {
	# 	"id": 2,
	# 	"Assigned By": "Charlie",
	# 	"Member": "Mary",
	# 	"Task": "Fix pitch and practice with partner"
	# },
	# {
	# 	"id": 3,
	# 	"Assigned By": "Ellie",
	# 	"Member": "Maggie",
	# 	"Task": "Practice solo in front of audience."
	# }
]

tasks = []


@app.route('/view_progress', methods=['GET', 'POST'])
def view_progress():
	return render_template('view_progress.html', tasks=tasks)


@app.route('/view_tasks')
def view_tasks():
	return render_template('viewtasks.html')



@app.route('/add_completed', methods=['GET', 'POST'])
def add_completed():
	global counts
	json_data = request.get_json()
	completedVal = json_data['completed']
	notcompletedVal = json_data['notcompleted']
	member = json_data["member"]
	if member not in counts:
		counts[member] = {"completed": 0, "notcompleted": 0}
	else:
		for mem in counts:
			if member == mem:
				# dictionary is the value
				counts[mem]["completed"] = counts[mem]["completed"] + completedVal
				counts[mem]["notcompleted"] = counts[mem]["notcompleted"] + notcompletedVal
	return counts


@app.route('/add_name', methods=['GET', 'POST'])
def add_name():
	global data
	global current_id

	json_data = request.get_json()
	name = json_data["name"]

	# add new entry to array with
	# a new id and the name the user sent in JSON
	current_id += 1
	new_id = current_id
	new_name_entry = {
		"name": name,
		"id": current_id
	}
	data.append(new_name_entry)

	return jsonify(data=data)


@app.route('/Soppranos', methods=['GET', 'POST'])
@login_required
def new_exercise():
	form=ExerciseForm()
	exercise = Exercise.query.all()
	posts = Post.query.all()

	if form.validate_on_submit():
		exercise=Exercise(title=form.title.data, date_due=form.date_due.data, description=form.description.data,  link= form.link.data, author=current_user)
		db.session.add(exercise)
		db.session.commit()
		flash('Your Memory Exercise has been created', 'success')
		return redirect(url_for('new_exercise'))

	return render_template('Soppranos.html', title='New Memory Exercise', form=form , exercise=exercise, legend="Add an Exercise", posts=posts)



@app.route('/tasks')
def tasks():
	return render_template('addtasks.html', sales=sales)


@app.route('/add_task', methods=['GET', 'POST'])
def add_entry():
	# add a new client/reams purchase
	global sales
	global current_id_2

	json_data = request.get_json()
	print(json_data)
	assigned_by = json_data["Assigned By"]
	member = json_data["Member"]
	task = json_data["Task"]

	new_entry = {
		"Assigned By": assigned_by,
		"Member": member,
		"Task": task,
		"id": current_id_2
	}
	current_id_2 += 1
	# insert at start of list
	sales.insert(0, new_entry)

	# print(sales)

	# add a client to autocomplete
	# if client not in clients:
	# 	clients.append(client)

	# RETURNS TWO THINGS: SALES AND CLIENTS
	return jsonify(sales=sales)


@app.route('/delete_sale', methods=['GET', 'POST'])
def delete_entry():
	global sales

	json_data = request.get_json()

	id_entry = json_data["id"]

	for entry in sales:
		if entry["id"] == id_entry:
			sales.remove(entry)

		# sales = [entry for entry in sales if entry["id"] != id_entry]

	return jsonify(sales=sales)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('UserHome'))
	form=RegistrationForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created!', 'success')
		# return redirect(next_page) if next_page else redirect(url_for('login'))
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('UserHome'))
	form=LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page=request.args.get('next')
			return redirect(url_for('UserHome'))
		else:
			flash("Login unsuccessful, check email and/or password", 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('Home'))

def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn=random_hex+f_ext
	picture_path=os.path.join(app.root_path, 'static/profile_pic', picture_fn)
	form_picture.save(picture_path)
	return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file=save_picture(form.picture.data)
			current_user.image_file=picture_file
		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pic/'+current_user.image_file)
	posts=Post.query.all()
	return render_template('account.html', title='Account', image_file=image_file, posts=posts, form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form=PostForm()
	if form.validate_on_submit():
		post=Post(title=form.title.data, content=form.content.data, content2=form.content2.data, author=current_user)
		db.session.add(post)
		db.session.commit() 
		flash('Your Assignment has been created', 'success')
		return redirect(url_for('UserHome'))
	return render_template('create_post.html', title='New Post', form=form, legend="New Assignment")


@app.route('/post/<int:post_id>')
def post(post_id):
	post=Post.query.get_or_404(post_id)
	return render_template('post.html', tilte=post.title, post=post)

@app.route('/exercise/<int:exercise_id>')
def exercise(exercise_id):
	exercise=Exercise.query.get_or_404(exercise_id)
	return render_template('exercise.html', tilte=exercise.title, exercise=exercise)


@app.route('/post/<int:post_id>/update',  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post=Post.query.get_or_404(post_id)

	form=PostForm()
	if form.validate_on_submit():
		post.title=form.title.data
		post.content=form.content.data
		post.content2=form.content2.data
		db.session.commit()
		flash("Your Assignment Has Been Updated!", 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data=post.title
		form.content.data=post.content
		form.content2.data=post.content2
	return render_template('create_post.html', title='Update Post', form=form, legend="Update Assignment")



@app.route('/exercise/<int:exercise_id>/update',  methods=['GET', 'POST'])
@login_required
def update_exercise(exercise_id):
	exercise=Exercise.query.get_or_404(exercise_id)

	form=ExerciseForm()
	if form.validate_on_submit():
		exercise.title=form.title.data
		exercise.date_due=form.date_due.data
		exercise.description=form.description.data
		exercise.link=form.link.data
		db.session.commit()
		flash("Your Exercise Has Been Updated!", 'success')
		return redirect(url_for('post', exercise_id=exercise.id))
	elif request.method == 'GET':
		form.title.data=exercise.title
		form.date_due.data=exercise.date_due
		form.description.data=exercise.description
		form.link.data=exercise.link
	return render_template('create_post.html', title='Update Exercise', form=form, legend="Update Exercise")

@app.route('/post/<int:post_id>/delete',  methods=['POST'])
@login_required
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)

	db.session.delete(post)
	db.session.commit()
	flash("Your Assignment Has Been Completed!", 'success')
	return redirect(url_for('UserHome'))

@app.route('/exercise/<int:exercise_id>/delete',  methods=['POST'])
@login_required
def delete_exercise(exercise_id):
	exercise=Exercise.query.get_or_404(exercise_id)

	db.session.delete(exercise)
	db.session.commit()
	flash("Your Exercise Has Been Deleted!", 'success')
	return redirect(url_for('new_exercise'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route("/exercise/<string:username>")
def user_exercises(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    exercise = Exercise.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_exercises.html', exercises=exercise, user=user)


@app.route('/Tempo', methods=['GET', 'POST'])
@login_required
def new_tempo():
	form=TempoForm()
	tempo = Tempo.query.all()
	posts = Post.query.all()
	if form.validate_on_submit():
		tempo=Tempo(title=form.title.data, date_due=form.date_due.data, description=form.description.data,  link= form.link.data, author=current_user)
		db.session.add(tempo)
		db.session.commit()
		flash('Your Tempo Exercise has been created', 'success')
		return redirect(url_for('new_tempo'))

	return render_template('Tempo.html', title='New Tempo Exercise', form=form , tempo=tempo, legend="Add an Exercise", posts=posts)

@app.route('/tempo/<int:tempo_id>')
def tempo(tempo_id):
	tempo=Tempo.query.get_or_404(tempo_id)
	return render_template('exercise_tempo.html', title=tempo.title, tempo=tempo)

@app.route('/tempo/<int:tempo_id>/update',  methods=['GET', 'POST'])
@login_required
def update_tempo(tempo_id):
	tempo=Tempo.query.get_or_404(tempo_id)

	form=TempoForm()
	if form.validate_on_submit():
		tempo.title=form.title.data
		tempo.date_due=form.date_due.data
		tempo.description=form.description.data
		tempo.link=form.link.data
		db.session.commit()
		flash("Your Exercise Has Been Updated!", 'success')
		return redirect(url_for('post', tempo_id=tempo.id))
	elif request.method == 'GET':
		form.title.data=tempo.title
		form.date_due.data=tempo.date_due
		form.description.data=tempo.description
		form.link.data=tempo.link
	return render_template('create_post.html', title='Update Exercise', form=form, legend="Update Exercise")

@app.route('/tempo/<int:tempo_id>/delete',  methods=['POST'])
@login_required
def delete_tempo(tempo_id):
	tempo=Tempo.query.get_or_404(tempo_id)

	db.session.delete(tempo)
	db.session.commit()
	flash("Your Exercise Has Been Deleted!", 'success')
	return redirect(url_for('new_tempo'))

@app.route("/tempo/<string:username>")
def user_tempos(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    tempo = Tempo.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_tempos.html', tempos=tempo, user=user)


@app.route('/Pitch', methods=['GET', 'POST'])
@login_required
def new_pitch():
	form=PitchForm()
	pitch = Pitch.query.all()
	posts = Post.query.all()
	if form.validate_on_submit():
		pitch=Pitch(title=form.title.data, date_due=form.date_due.data, description=form.description.data,  link= form.link.data, author=current_user)
		db.session.add(pitch)
		db.session.commit()
		flash('Your Pitch Exercise has been created', 'success')
		return redirect(url_for('new_pitch'))

	return render_template('Pitch.html', title='New Pitch Exercise', form=form , pitch=pitch, legend="Add an Exercise", posts=posts)

@app.route('/pitch/<int:pitch_id>')
def pitch(pitch_id):
	pitch=Pitch.query.get_or_404(pitch_id)
	return render_template('exercise_pitch.html', title=pitch.title, pitch=pitch)

@app.route('/pitch/<int:pitch_id>/update',  methods=['GET', 'POST'])
@login_required
def update_pitch(pitch_id):
	pitch=Tempo.query.get_or_404(pitch_id)

	form=PitchForm()
	if form.validate_on_submit():
		pitch.title=form.title.data
		pitch.date_due=form.date_due.data
		pitch.description=form.description.data
		pitch.link=form.link.data
		db.session.commit()
		flash("Your Exercise Has Been Updated!", 'success')
		return redirect(url_for('post', pitch_id=pitch.id))
	elif request.method == 'GET':
		form.title.data=pitch.title
		form.date_due.data=pitch.date_due
		form.description.data=pitch.description
		form.link.data=pitch.link
	return render_template('create_post.html', title='Update Exercise', form=form, legend="Update Exercise")

@app.route('/pitch/<int:pitch_id>/delete',  methods=['POST'])
@login_required
def delete_pitch(pitch_id):
	pitch=Pitch.query.get_or_404(pitch_id)

	db.session.delete(pitch)
	db.session.commit()
	flash("Your Exercise Has Been Deleted!", 'success')
	return redirect(url_for('new_pitch'))

@app.route("/pitch/<string:username>")
def user_pitches(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    pitch = Pitch.query.filter_by(author=user)\
        .order_by(Pitch.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_pitches.html', pitches=pitch, user=user)


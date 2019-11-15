from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)

@app.route('/Home')
def Home2():
	return render_template('Home.html')
@app.route('/')
def Home():
	return render_template('Home.html')

@app.route('/leader_board')
def leaderboard():
	return render_template('leader_dashboard.html')
@app.route('/view_tasks')
def view_tasks():
	return render_template('dragdrop.html')

@app.route('/member_board')
def memberboard():
	return render_template('member_dashboard.html')

@app.route('/task_complete')
def task_complete():
	return render_template('member_dashboard.html')


current_id = 2
data = [
	{
		"id": 1,
		"name": "michael scott"
	},
	{
		"id": 2,
		"name": "jim halpert"
	},
]

current_id_2 = 4
sales = [
	{
		"id": 1,
		"Assigned By": "Casey",
		"Member": "Julia",
		"Task": "Learn notes for Rolling Stone"
	},
	{
		"id": 2,
		"Assigned By": "Charlie",
		"Member": "Mary",
		"Task": "Fix pitch and practice with partner"
	},
	{
		"id": 3,
		"Assigned By": "Ellie",
		"Member": "Maggie",
		"Task": "Practice solo in front of audience."
	}
]
clients = [
	"Shake Shack",
	"Toast",
	"Computer Science Department",
	"Teacher's College",
	"Starbucks",
	"Subsconsious",
	"Flat Top",
	"Joe's Coffee",
	"Max Caffe",
	"Nussbaum & Wu",
	"Taco Bell",
]


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

	# send back the WHOLE array of data, so the client can redisplay it
	return jsonify(data=data)


@app.route('/infinity')
def paper():
	return render_template('cu-paper-infinity.html', sales=sales, clients=clients)


@app.route('/save_sale', methods=['GET', 'POST'])
def add_entry():
	# add a new client/reams purchase
	global sales
	global current_id_2

	global clients

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

	print(sales)

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





if __name__ == '__main__':
	app.run(debug=True)

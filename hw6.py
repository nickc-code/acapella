# Michaella Schaszberger
# mls2290
# UI Design, HW6
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify

app = Flask(__name__)

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
         "salesperson": "James D. Halpert",
         "client": "Shake Shack",
         "reams": 1000
     },
     {
         "id": 2,
         "salesperson": "Stanley Hudson",
         "client": "Toast",
         "reams": 4000
     },
     {
         "id": 3,
         "salesperson": "Michael G. Scott",
         "client": "Computer Science Department",
         "reams": 10000
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

non_ppc_people = [
"Phyllis",
"Dwight",
"Oscar",
"Creed",
"Pam",
"Jim",
"Stanley",
"Michael",
"Kevin",
"Kelly"
]
ppc_people = [
"Angela"
]


@app.route('/')
def hello_world():
   return 'Hello World'


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name) 


@app.route('/hw6_app')
def people():
    return render_template('people.html', data=data)  


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
        "id":  current_id
    }
    data.append(new_name_entry)

    #send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data = data)
 

@app.route('/infinity')
def paper():
    return render_template('cu-paper-infinity.html', sales=sales, clients=clients)


@app.route('/save_sale', methods = ['GET','POST'])
def add_entry():
    #add a new client/reams purchase
    global sales
    global current_id_2

    global clients

    json_data = request.get_json()
    client = json_data["client"]
    reams = json_data["reams"]

    new_entry = {
        "salesperson": "Michaella Schaszberger",
        "client": client,
        "reams": reams,
        "id": current_id_2
    }
    current_id_2 += 1
    #insert at start of list
    sales.insert(0,new_entry)

    #add a client to autocomplete
    if client not in clients:
        clients.append(client)

    #RETURNS TWO THINGS: SALES AND CLIENTS
    return jsonify(sales = sales), clients


@app.route('/delete_sale', methods = ['GET','POST'])
def delete_entry():
    global sales

    json_data = request.get_json()

    id_entry = json_data["id"]

    for entry in sales:
        if entry["id"] == id_entry:
            sales.remove(entry)

    # sales = [entry for entry in sales if entry["id"] != id_entry]

    return jsonify(sales = sales)


@app.route('/ppc')
def committee():
    return render_template('ppc.html', non_ppc_people=non_ppc_people, ppc_people=ppc_people)


@app.route('/moveto_ppc', methods = ['GET','POST'])
def move_ppc():
    global non_ppc_people
    global ppc_people

    json_data = request.get_json()

    name = json_data["name"]

    for person in non_ppc_people:
        if person == name:
            non_ppc_people.remove(person)

    ppc_people.append(name)

    return ppc_people,non_ppc_people


@app.route('/moveto_nonppc', methods=['GET', 'POST'])
def move_nonppc():
    global non_ppc_people
    global ppc_people

    json_data = request.get_json()

    name = json_data["name"]

    for person in ppc_people:
        if person == name:
            ppc_people.remove(person)

    non_ppc_people.append(name)

    return ppc_people, non_ppc_people

if __name__ == '__main__':
   app.run(debug = True)





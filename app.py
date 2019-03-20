"""

	Mantas Svedas Info 3gr. Elektronines vaistines web servisas "EPharma"
	
	Resources: Clients, ClientById, ClientByIdOrders
	
	/	
	/index
	/clients 
	/clients/<id>/
	/clients/<id>/orders

	Clients
		GET 		// Shows all clients
		POST		// Add a client 
		DELETE		// Deletes all clients
		
	ClientById
		GET		// Gets client data 
		POST 		// `Adds client order`
		DELETE		// Deletes client
		PUT			// Edits client data
	
	ClientByIdOrders
		GET		// Shows client orders
		POST		// `Adds client order`
		DELETE		// Deletes all client orders
"""

from flask import Flask, request, g
from flask_restful import Resource, Api, reqparse
import os, json
import markdown
import shelve

app = Flask(__name__)
api = Api(app)

@app.route("/index")
def index():
	"""Present some documentation"""
	#Opens the README file
	with open(os.path.dirname(app.root_path) + '/code/README.md', 'r') as markdown_file:
	#with open(os.path.dirname(app.root_path) + '\EPharma\README.md', 'r') as markdown_file:
		#Reads the content of the file
		content = markdown_file.read()
		#Converts to HTML
		return markdown.markdown(content)
		
		
class Clients(Resource):
	def get(self):
		shelf = get_db()
	
		clients_counter = 0
		#Checks if there are any clients
		if "clients_counter" in shelf:
			clients_counter = shelf["clients_counter"]
		if clients_counter == 0:
			return {'message': "Not found, try going to root URL", 'data': []}, 404
			
		#Collects and returns clients
		clients = []
		for x in range(1, clients_counter+1):
			client_key = "client" + str(x)
			if client_key in shelf:
				clients.append(shelf[client_key])
				
		if len(clients) == 0:
			return {'message': "Not found, no clients", 'data': []}, 404
		return {'message': "OK", 'data': clients}, 200
		
		
	def post(self):
		shelf = get_db()
		
		#Request validation
		parser = reqparse.RequestParser()
		parser.add_argument('name', required=True)
		parser.add_argument('address', required=True)
		parser.add_argument('email', required=True)
		
		#Adds a client
		args = parser.parse_args()
		client_nr = shelf["clients_counter"]
		client_nr += 1
		shelf["clients_counter"] = client_nr
		client_key = "client" + str(client_nr)
		args.update({'id': client_key})
		#args = json.dumps(args)
		
		print(args)
		#if client_key in shelf:
		shelf[client_key] = args
		client_orders_counter = client_key + "_counter" # client<?>_counter
		shelf[client_orders_counter] = 0
		
		return {'message': "Created", 'data': args}, 201, {'Location': "/clients/" + str(client_nr)}
		
	
	def delete(self):
		shelf = get_db()
		
		#Checks if there are any clients
		client_nr = shelf["clients_counter"]
		if client_nr == 0:
			return {'message': "Not found, no clients", 'data': []}, 404
			
		#Deletes all clients
		for x in range(1, client_nr+1):
			client_key = "client" + str(x)
			if client_key in shelf:
				del shelf[client_key]
		shelf["clients_counter"] = 0		
		return {'message': "No content", 'data': []}, 204
		
	
	def put(self):
		return {'message': "Not Allowed", 'data': []}, 405
		

class ClientById(Resource):
	def get(self, id):
		shelf = get_db()
		
		#Checks for client
		client_key = "client" + id
		if client_key not in shelf:
			return {'message': "Not Found, no such client", 'data': []},404
			
		#Returns client info
		args = shelf[client_key]
		return {'message': "OK", 'data': args}, 200
		
		
	def post(self, id):
		shelf = get_db()
		
		#Checks for client
		client_key = "client" + id
		if client_key not in shelf:
			return {'message': "Not Found, no such client", 'data': []},404
		
		#Request validation
		parser = reqparse.RequestParser()
		parser.add_argument('item', required=True)
		parser.add_argument('price', required=True)
		parser.add_argument('amount', required=True)
		args = parser.parse_args()
		#args = json.dumps(args)
		
		#Adds order
		db_client_order_counter = "client" + id + "_counter"
		order_nr = shelf[db_client_order_counter]
		order_nr += 1
		shelf[db_client_order_counter] = order_nr
		order_key = "client" + id + "_order" + str(order_nr)	# client<?>_order<?>
		
		#if order_key in shelf:
		shelf[order_key] = args
		
		return {'message': "Created", 'data': args}, 201, {'Location': "/clients/" + str(id) + "/orders"}
		
		
	def delete(self, id):
		shelf = get_db()
		
		#Checks for client
		client_key = "client" + id
		if client_key not in shelf:
			return {'message': "Not Found, no such client", 'data': []},404

		#Deletes all client's orders
		db_client_orders_counter = "client" + id + "_counter"	#example "client8_counter"
		order_counter = shelf[db_client_orders_counter]
		for x in range(1, order_counter+1):
			order_key = "client" + id + "_order"+ str(x)
			if order_key in shelf:
				del shelf[order_key]
		shelf[db_client_orders_counter] = 0		
		
		#Deletes client
		del shelf[client_key]
		del shelf[db_client_orders_counter]
		
		return {'message': "No content", 'data': []}, 204

		
	def put(self,id):
		shelf = get_db()
		
		#Checks for client
		client_key = "client" + id
		if client_key not in shelf:
			return {'message': "Not Found, no such client", 'data': []},404
		
		#Request validation
		parser = reqparse.RequestParser()
		parser.add_argument('name', required=True)
		parser.add_argument('address', required=True)
		parser.add_argument('email', required=True)
		args = parser.parse_args()
		args.update({'id': client_key})
		#args = json.dumps(args)
		
		#Edits client
		shelf[client_key] = args
		return {'message': "Created", 'data': args}, 201


class ClientByIdOrders(Resource):
	def get(self,id):
		shelf = get_db()
		
		#Checks for client
		client_key = "client" + id
		if client_key not in shelf:
			return {'message': "Not Found, no such client", 'data': []},404
			
		#Checks for orders
		db_client_orders_counter = "client" + id + "_counter"	#example "client8_counter"
		order_counter = shelf[db_client_orders_counter]
		if order_counter == 0:
			return {'message': "Not found, no orders", 'data': []}, 404
			
		#Shows client orders
		orders = []
		for x in range(1, order_counter+1):
			order_key = "client" + id + "_order"+ str(x)
			if order_key in shelf:
				orders.append(shelf[order_key])
				
		if len(orders) == 0:
			return {'message': "Not found", 'data': []}, 404
		return {'message': "OK", 'data': orders}, 200
	
	
	def post(self,id):
		shelf = get_db()
		
		#Checks for client
		client_key = "client" + id
		if client_key not in shelf:
			return {'message': "Not Found, no such client", 'data': []},404
		
		#Request validation
		parser = reqparse.RequestParser()
		parser.add_argument('item', required=True)
		parser.add_argument('price', required=True)
		parser.add_argument('amount', required=True)
		args = parser.parse_args()
		#args = json.dumps(args)
		
		#Adds order
		db_client_order_counter = "client" + id + "_counter"
		order_nr = shelf[db_client_order_counter]
		order_nr += 1
		shelf[db_client_order_counter] = order_nr
		order_key = "client" + id + "_order" + str(order_nr)	# client<?>_order<?>
		
		#if order_key in shelf:
		shelf[order_key] = args
		
		return {'message': "Created", 'data': args}, 201, {'Location': "/clients/" + str(id) + "/orders"}
		
	
	def delete(self, id):
		shelf = get_db()
		
		#Checks for client
		client_key = "client" + id
		if client_key not in shelf:
			return {'message': "Not Found, no such client", 'data': []},404

		#Checks for orders
		db_client_orders_counter = "client" + id + "_counter"	#example "client8_counter"
		order_counter = shelf[db_client_orders_counter]
		if order_counter == 0:
			return {'message': "Not found, no orders", 'data': []}, 404
		
		#Deletes all client's orders
		for x in range(1, order_counter+1):
			order_key = "client" + id + "_order"+ str(x)
			if order_key in shelf:
				del shelf[order_key]
		shelf[db_client_orders_counter] = 0		
		return {'message': "No content", 'data': []}, 204
		
	
	def put(self):
		return {'message': "Not Allowed", 'data': []}, 405
		
		
class WelcomeScreen(Resource):
	def get(self):	
		shelf = get_db()
		db_client_counter = "clients_counter"
		if db_client_counter not in shelf:
			demo()
			return {'message': "Welcome to this new site, go to ./index for information", 'data': []}, 200
		return {'message': "Welcome to this site, go to ./index for information", 'data': []}, 200
		
	
	#debug func
	def post(self):
		some_json = request.get_json()
		return {'message': "you sent request", 'data': some_json}, 201
	
	def delete(self):
		return {'message': "Not Allowed", 'data': []}, 405
	
	def put(self):
		return {'message': "Not Allowed", 'data': []}, 405
				
		
api.add_resource(WelcomeScreen, '/')
api.add_resource(Clients, '/clients')
api.add_resource(ClientById, '/clients/<string:id>')
api.add_resource(ClientByIdOrders, '/clients/<string:id>/orders')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("shelf.db")
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
	
def demo():
	shelf = get_db()
	shelf["clients_counter"] = 0
	shelf["client1"] = {'name': 'Tester1', 'address': 'MIF INFO 3', 'email': 'testing@mif.vu.lt', 'id': 'client1'}
	shelf["client2"] = {'name': 'Tester1', 'address': 'MIF INFO 3', 'email': 'testing@mif.vu.lt', 'id': 'client2'}
	shelf["client3"] = {'name': 'Tester1', 'address': 'MIF INFO 3', 'email': 'testing@mif.vu.lt', 'id': 'client3'}
	shelf["client2_order1"] = {'item': 'Pills', 'price': '16.90', 'amount': '10'}
	shelf["client2_order2"] = {'item': 'Cough Syrup', 'price': '20.90', 'amount': '5'}
	shelf["client3_order1"] = {'item': 'Mega Pills', 'price': '4.90', 'amount': '2'}
	shelf["clients_counter"] = 3
	shelf["client1_counter"] = 0
	shelf["client2_counter"] = 2
	shelf["client3_counter"] = 1
	return
	
if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)
	#app.run(host="localhost", debug=True)
	

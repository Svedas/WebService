"""

	Mantas Svedas Info 3gr. Elektronines vaistines web servisas "EPharme"
	
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
		GET			// Gets client data 
		POST 		// `Adds client order`
		DELETE		// Deletes client
		PUT			// Edits client data
	
	ClientByIdOrders
		GET			// Shows client orders
		POST		// `Adds client order`
		DELETE		// Deletes all client orders
"""

from flask import Flask, request
from flask_restful import Resource, Api
from redis import Redis
import os, json
import markdown

app = Flask(__name__)
api = Api(app)
redis = Redis(host='localhost', port=6379)
#re=StrictRedis(host="localhost", port=6379).keys()

@app.route("/index")
def index():
	"""Present some documentation"""
	#Opens the README file
	with open(os.path.dirname(app.root_path) + '\EPharma\README.md', 'r') as markdown_file:
		#Reads the content of the file
		content = markdown_file.read()
		#Converts to HTML
		return markdown.markdown(content)


class WelcomeScreen(Resource):
	def get(self):
		return "Welcome to this site, go to ./index for information"
	
	#debug func
	def post(self):
		some_json = request.get_json()
		return [{'info': "you sent"},some_json], 201
		
		
class Clients(Resource):
	def get(self):
		#Checks if there are any clients
		redis_clients_counter = 'clients_counter'
		if redis.exists(redis_clients_counter) == 0:
			return "Not found", 404	
		clients_counter = redis.get(redis_clients_counter).decode('UTF-8')
		#Collects and returns clients
		clients = []
		for x in range(1, int(clients_counter)+1):
			client_key = "'"+ "client" + str(x) + "'"
			if  redis.exists(client_key) == 1:
				clients.append(json.loads(redis.get(client_key)))
		#return {"info": "Clients info. Total {} Clients".format(redis.get('clients_counter').decode('UTF-8'))}
		if len(clients) == 0:
			return "Not found", 404
		return clients, 200
		
	def post(self):
		redis_clients_counter = 'clients_counter'
		redis.incr(redis_clients_counter)
		#client_json = json.dumps( request.get_json() )
		client_nr = redis.get(redis_clients_counter).decode('UTF-8')
		client_key = "'"+ "client" + client_nr + "'"
		#client_nr = "{}".format( redis.get('clients_counter') )[2:-1] #alternative formating
		#Json request modification
		content = request.data  
		content_json = json.loads(content)
		content_json.update({'id': client_key})
		client_json = json.dumps(content_json)
		#Adds client
		redis.set(client_key, client_json)
		client_orders_counter = client_key[:-1] + "_counter'" # returns 'client<?>_counter'
		redis.set(client_orders_counter, 0)
		#return {"info": "Client added with id {}, {} ".format(client_nr,client_key)}, 201
		return "Created", 201
	
	def delete(self):
		#Checks if there are any clients
		redis_clients_counter = 'clients_counter'
		if redis.exists(redis_clients_counter) == 0:
			return "Not found", 404
		#Deletes all clients
		clients_counter = redis.get(redis_clients_counter).decode('UTF-8')
		for x in range(1, int(clients_counter)+1):
			client_key = "'"+ "client" + str(x) + "'"
			if redis.exists(client_key) == 1:
				redis.delete(client_key)
		redis.set('clients_counter',0)		
		return "No content", 204
		

class ClientById(Resource):
	def get(self, id):
		#Checks for client
		client_key = "'"+ "client" + id + "'"
		if  redis.exists(client_key) == 0:
			return "Not Found",404
		#Returns client info
		client_by_id_json = json.loads(redis.get(client_key))
		return client_by_id_json, 200
		
	def post(self, id):
		order_json = json.dumps( request.get_json() )
		#Checks for client
		if redis.exists("'"+ "client"+id+"'") == 0:
			return "Not found", 404
		redis_client_order_counter = "'"+ "client" + id + "_counter'"
		if redis.exists(redis_client_order_counter) == 0:
			return "Not found", 404
		redis.incr(redis_client_order_counter)
		#Adds order
		client_order_nr = redis.get(redis_client_order_counter).decode('UTF-8')
		order_key = "'"+ "client" + id + "_order"+ client_order_nr + "'"	# gives 'client<?>_order<?>'
		redis.set(order_key, order_json)
		#return {"info": "Order {} for client {} added ".format(client_order_nr, id)}, 201
		return "Created", 201
		
	def delete(self, id):
		client_key = "'"+ "client" + id + "'"
		if  redis.exists(client_key) == 1:
			#Deletes orders, then client
			ClientByIdOrders.delete(self,id)
			redis.delete(client_key)
			return "No content", 204
		return "Not Found",404
		
	def put(self,id):
		#Checks for client
		client_key = "'"+ "client" + id + "'"
		if redis.exists(client_key) == 0:
			return "Not found", 404
		#Json request modification
		content = request.data  
		content_json = json.loads(content)
		content_json.update({'id': client_key})
		client_json = json.dumps(content_json)
		#Edits client
		redis.set(client_key, client_json)
		#return {"info": "Client edited with id {} ".format(id)}, 201
		return "Created", 201


class ClientByIdOrders(Resource):
	def get(self,id):
		#Checks for client
		if redis.exists("'"+ "client"+id+"'") == 0:
			return "Not found", 404
		redis_client_orders_counter = "'"+ "client" + id + "_counter'"		#example "'client8_counter'"
		if int(redis.get(redis_client_orders_counter).decode('UTF-8')) == 0:
			return "Not found, no orders", 404
		client_orders_counter = redis.get("'"+ "client" + id + "_counter'").decode('UTF-8')
		#Shows client orders
		orders = []
		for x in range(1, int(client_orders_counter)+1):
			order_key = "'"+ "client" + id + "_order"+ str(x) + "'"
			if redis.exists(order_key) == 1:
				orders.append(json.loads(redis.get(order_key)))
		#return [{"info": "You should see client's {} orders".format(id)}, orders]
		if len(orders) == 0:
			return "Not found", 404
		return orders, 200
	
	
	def post(self,id):
		order_json = json.dumps( request.get_json() )
		#Checks for client
		if redis.exists("'"+ "client"+id+"'") == 0:
			return "Not found", 404
		redis_client_orders_counter = "'" + "client" + id + "_counter'"
		if redis.exists(redis_client_orders_counter) == 0:
			return "Not found", 404
		redis.incr(redis_client_orders_counter)
		#Adds order
		client_order_nr = redis.get(redis_client_orders_counter).decode('UTF-8')
		order_key = "'"+ "client" + id + "_order" + client_order_nr + "'"
		redis.set(order_key, order_json)
		#return {"info": "Client {} order {} added ".format(id, client_order_nr)}, 201
		return "Created", 201		
	
	def delete(self, id):
		#Checks if client exists
		if redis.exists("'"+ "client"+id+"'") == 0:
			return "Not found", 404
		#Checks if there are orders
		redis_client_orders_counter = "'" + "client" + id + "_counter'"
		if int(redis.get(redis_client_orders_counter).decode('UTF-8')) == 0:
			return "Not found, no orders", 404
		#Deletes all client's orders
		client_orders_counter = redis.get(redis_client_orders_counter).decode('UTF-8')
		for x in range(1, int(client_orders_counter)+1):
			order_key = "'"+ "client" + id + "_order"+ str(x) + "'"
			if redis.exists(order_key) == 1:
				redis.delete(order_key)
		redis.set(redis_client_orders_counter,0)		
		return "No content", 204
				
		
api.add_resource(WelcomeScreen, '/')
api.add_resource(Clients, '/clients')
api.add_resource(ClientById, '/clients/<string:id>')
api.add_resource(ClientByIdOrders, '/clients/<string:id>/orders')
	
	
if __name__ == '__main__':
	app.run(debug=True)
	#app.run(host="localhost", debug=True)
	
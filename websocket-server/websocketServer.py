from websocket_server import WebsocketServer
import json

comms = {}

def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])


def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])

def log(js, id):
	print("%s (%s / %d) sent:  '%s' %s" % (js['node'], js['notebook_id'], id, js['task'], js['msg']))

def message_received(client, server, message):
	js = json.loads(message)
	log(js, client['id'])
	notebook_id = js['notebook_id']
	if js.get('task') == 'init':
		if not comms.get(notebook_id):
			comms[notebook_id] = {"notebook":None, "interpreter":None}
		comms[notebook_id][js['node']] = client
		print("Init:", comms[notebook_id])
	else:
		
		forwardMsg = json.dumps({"notebook_id":js['notebook_id'], "task":js['task'], "msg":js['msg']})
		notebook_id = js['notebook_id']
		if js['node'] == 'notebook':
			server.send_message(comms[notebook_id]['interpreter'], forwardMsg)
		elif js['node'] == 'interpreter':
			server.send_message(comms[notebook_id]['notebook'], forwardMsg)
		else:
			print("Wrong message")

PORT=9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
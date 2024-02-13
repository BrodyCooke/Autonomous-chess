from flask import Flask, render_template, request, jsonify
from clients import Client
import json

app = Flask(__name__)

# List to store instances of Client class
clients = []

# Route for handling the initial connection and sending the HTML page
@app.route('/')
def index():
    # Find or create client instance
    client_ip = request.remote_addr
    client = None
    for c in clients:
        if c.ip == client_ip:
            client = c
            break
    if not client:
        client = Client(client_ip)
        clients.append(client)
    if(len(clients) == 1):
        return render_template('index.html')
    else:
        return render_template('index2.html')

# Route for handling incoming messages from the client
@app.route('/message', methods=['POST'])
def message():
    client_ip = request.remote_addr
    message_data = request.json

    # Find or create client instance
    client = None
    for c in clients:
        if c.ip == client_ip:
            client = c
            break
    if not client:
        client = Client(client_ip)
        clients.append(client)

    message = message_data['message']
    client.add_message(message)
    for client in clients:
        print(client.get_messages())

    return jsonify({'status': 'Message received', 'message': message})

# Route for sending messages back to the client
@app.route('/status', methods=['GET'])
def status():
    client_ip = request.remote_addr

    # Find the client instance
    client = None
    other_client = None
    for c in clients:
        if c.ip == client_ip:
            client = c
        else:
            other_client = c
    if other_client == None:
        return jsonify({'status': 'Message sent', 'message': ''})
        
    message = other_client.get_lastmessage()
    other_client.zero_lastmessage()
    #message = "56 48"
    #message = ''

    # Check if the client instance exists
    if client:
        # Here you can customize the response to the client
        return jsonify({'status': 'Message sent', 'message': message})

    else:
        return jsonify({'status': 'Error', 'message': 'Client not found'})
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)

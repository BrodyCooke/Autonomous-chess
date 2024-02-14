from flask import Flask, render_template, request, jsonify
from clients import Client

app = Flask(__name__)

# List to store instances of Client class
clients = []

# Route for handling the initial connection and sending the HTML page
@app.route('/')
def index():
    # Find or create client instance
    client_ip = request.remote_addr
    client = None

    # Find or create client
    for c in clients:
        if c.ip == client_ip:
            client = c
            break
    if not client:
        client = Client(client_ip)
        clients.append(client)

    if(len(clients) % 2 == 1):
        return render_template('index.html')
    elif(len(clients) % 2 == 0):
        client.set_pair(clients[0])
        clients[0].set_pair(client)
        return render_template('index2.html')

# Route for handling incoming messages from the client
@app.route('/message', methods=['POST'])
def message():
    client_ip = request.remote_addr
    message_data = request.json

    # Find client instance
    client = None
    for c in clients:
        if c.ip == client_ip:
            client = c
            break

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
            break

    other_client = client.get_pair()
    if other_client == None:
        return jsonify({'status': 'no new message', 'message': ''})
        
    message = other_client.get_lastmessage()
    other_client.zero_lastmessage()

    # Check if the client instance exists
    if client:
        return jsonify({'status': 'new message', 'message': message})

    else:
        return jsonify({'status': 'Error', 'message': 'Client not found'})
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=False)

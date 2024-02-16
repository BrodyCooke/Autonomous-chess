from flask import Flask, render_template, request, jsonify,  redirect, url_for
from clients import Client
from game import Game

from datetime import datetime

app = Flask(__name__)

# List to store instances of Client class
game = Game()

# Route for handling the initial connection and sending the HTML page
@app.route('/')
def index():
    # Find or create client instance
    client_ip = request.remote_addr
    client = None

    # Find or create client
    for c in game.get_clients():
        if c.ip == client_ip:
            client = c
            break
    if not client:
        client = Client(client_ip)
        game.add_client(client)

    # first gets sent setup page
    if(len(game.get_clients()) == 1):
        return render_template('homepage.html')
    # second and on gets blank page
    elif(len(game.get_clients()) > 1):
        return render_template('waiting.html')
    
# Route for assigning client type for each client. should be done for every client
@app.route('/identify', methods=['POST'])
def identify():
    client_ip = request.remote_addr
    message_data = request.json
    client = None
    # Find client instance
    #make sure this is a valid client
    for c in game.get_clients():
        if c.ip == client_ip:
            client = c
            break
    if not client:
        return jsonify({'status': 'Error', 'message': 'Client not found'})   
    
    message = message_data['message']
    client.set_type(message)
    return jsonify({'status': 'Message received', 'message': message})

# Route for telling clients when game starts
@app.route('/startup', methods=['POST'])
def startup():
    client_ip = request.remote_addr
    message_data = request.json

    #make sure client is valid
    for c in game.get_clients():
        if c.ip == client_ip:
            client = c
            break
    if not client:
        return jsonify({'status': 'Error', 'message': 'Client not found'})

    white_type = message_data['white']
    black_type = message_data['black']

    #find the first client that is of white type
    print('White type: ', white_type)
    print(c.get_type())
    for c in game.get_clients():
        if c.get_type() == white_type:
            white_client = c
            game.set_white(white_client)
            print('setting white')
            break
    #find the first client that is of black type
    for c in game.get_clients():
        if c.get_type() == black_type:
            black_client = c
            game.set_black(black_client)
            break

    return jsonify({'status': 'Message received', 'message': message_data})

# Route for telling clients when game starts
@app.route('/waiting', methods=['GET'])
def waiting():
    client_ip = request.remote_addr 
    client = None
    # Find client instance
    #make sure this is a valid client
    for c in game.get_clients():
        if c.ip == client_ip:
            client = c
            break
    if not client:
        return jsonify({'status': 'Error', 'message': 'Client not found'})

    for c in game.get_clients():
        if c.ip == client_ip:
            if c == game.get_white():
                return redirect(url_for('white_player'))
            elif c == game.get_black():
                return redirect(url_for('black_player'))
    return jsonify({'status': 'Error', 'message': 'Game not started yet'})    

# Route for the white player
@app.route('/white_player')
def white_player():
    return render_template('white.html')   

# Route for the black player
@app.route('/black_player')
def black_player():
    return render_template('black.html')       

    
# Route for handling incoming messages from the client
@app.route('/sendmove', methods=['POST'])
def message():
    client_ip = request.remote_addr
    message_data = request.json

    client = None
    # Find client instance
    # make sure this is a valid client
    for c in game.get_clients():
        if c.ip == client_ip:
            client = c
            break
    if not client:
        return jsonify({'status': 'Error', 'message': 'Client not found'})         
    
    # Store the message in the gamestate and reply to client
    message = message_data['message']
    game.add_message(message)
    game.set_lastmessage(message)

    return jsonify({'status': 'Message received', 'message': message})

# Route for sending messages back to the client
@app.route('/receivemove', methods=['GET'])
def status():
    start = datetime.now()
    client_ip = request.remote_addr

    # Find the client instance
    client = None
    for c in game.get_clients():
        if c.ip == client_ip:
            client = c
            break
        
    message = game.get_lastmessage()
    #message = '12 23'
    game.zero_lastmessage()

    # Check if the client instance exists
    end = datetime.now()
    print("Runtime is: ",(end-start))
    if client:
        return jsonify({'status': 'new message', 'message': message})

    else:
        return jsonify({'status': 'Error', 'message': 'Client not found'})


'''
@app.route('/apicall', methods=['GET'])
def apicall(): 
    
    micro_move = micro.previousmove()
        # This function needs to take in a move the micro made in UCL format and then output a move in UCL format to send back to micro
    rtv = call_api(micros_move)
    # return move back to micro
    return rtv
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=False)

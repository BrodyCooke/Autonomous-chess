from flask import Flask, render_template, request, jsonify,  redirect, url_for
from clients import Client
from game import Game
from chess_api import API

import time

app = Flask(__name__)

# List to store instances of Client class
game = Game()
API_game = API()

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
    # second and on gets waiting page
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
    print(message)
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

    if (black_type == 'ai'):
        API_client = Client('0.0.0.0')
        API_client.set_type('ai')
        API_client.set_color('black')
        game.add_client(API_client)
    if (white_type == 'ai'):
        API_client = Client('0.0.0.0')
        API_client.set_type('ai')
        API_client.set_color('white')
        game.add_client(API_client)

    # find the first client that is of white type
    for c in game.get_clients():
        if c.get_type() == white_type:
            white_client = c
            game.set_white(white_client)
            print('setting white')
            break
    # find the first client that is of black type and not already white
    for c in game.get_clients():
        if (c.get_type() == black_type) & (c != game.get_white()):
            black_client = c
            game.set_black(black_client)
            print('setting black')
            break
    # assign the other clients to spectators
    for c in game.get_clients():
        if (c != game.get_black()) & (c != game.get_white()):
            game.add_spectator(c)
            print('adding spectator')
    print(game.get_spectators())

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
    
    # If client is chessboard send text that the chessboard can interpret
    if(client.get_type() == 'chessboard'):
        if client == game.get_white():
            return jsonify({'status': 'Message received', 'message': 'white_player'})
        elif client == game.get_black():
            return jsonify({'status': 'Message received', 'message': 'black_player'})
        if(client in game.get_spectators()):
            return jsonify({'status': 'Message received', 'message': 'spectator_player'})
        return jsonify({'status': 'Message received', 'message': 'Game not started yet'})
    # if client is not a chessboad, redirect to webpages as needed
    else:
        if client == game.get_white():
            return redirect(url_for('white_player'))
        elif client == game.get_black():
            return redirect(url_for('black_player'))
        if(client in game.get_spectators()):
            return redirect(url_for('spectator_player'))
                
        return jsonify({'status': 'Error', 'message': 'Game not started yet'})    

# Route for the white player
@app.route('/white_player')
def white_player():
    return render_template('white_small.html')   

# Route for the black player
@app.route('/black_player')
def black_player():
    return render_template('black_small.html')      

# Route for the black player
@app.route('/spectator_player')
def spectator_player():
    return render_template('spectator.html')     

    
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

    message = message_data['message']

    if(game.get_white().get_type() == 'ai'):
        API_game.make_playermove(message)
   
    # Store the message in the gamestate and reply to client
    game.add_message(message)
    game.set_lastmessage(message)
    c.set_previousmove(message)

    return jsonify({'status': 'Message received', 'message': message})

# Route for sending messages back to the client
@app.route('/receivemove', methods=['GET'])
def status():
    start = time.time()
    client_ip = request.remote_addr

    # Find the client instance
    client = None
    for c in game.get_clients():
        if c.ip == client_ip:
            client = c
            break
    if not client:
        return jsonify({'status': 'Error', 'message': 'Client not found'})

    # Find the AI client instance
    if (game.get_white().get_type() == 'ai' or game.get_black().get_type() == 'ai'):
        AI_client = None
        for c in game.get_clients():
            if c.ip == '0.0.0.0':
                AI_client = c
                break
        if not AI_client:
            return jsonify({'status': 'Error', 'message': 'AI Client not found'})
        
    message = game.get_lastmessage()
    if(game.get_white().get_type() == 'ai'):
        if(message != AI_client.get_previousmove() and message != ''):
            print('message sent to AI is: ', message)
            new_move = API_game.get_api_move()
            message = new_move
            print('message sent from AI is: ', message)
            game.add_message(message)
            game.set_lastmessage(message)
            AI_client.set_previousmove(message)
            return jsonify({'status': 'new message', 'message': ''})
            #game.zero_lastmessage()

    elif(game.get_black().get_type() == 'ai'):
        if(message != AI_client.get_previousmove() and message != ''):
            print('message sent to AI is: ', message)
            API_game.make_playermove(message)
            new_move = API_game.get_api_move()
            message = new_move
            print('message sent from AI is: ', message)
            game.add_message(message)
            game.set_lastmessage(message)
            AI_client.set_previousmove(message)
            return jsonify({'status': 'new message', 'message': ''})
            #game.zero_lastmessage()
    else:
        if message == client.get_previousmove():
            return jsonify({'status': 'new message', 'message': ''})            

    end = time.time()
    print("Runtime is: ",(end-start))
    if client:
        game.zero_lastmessage()
        print('returning move')
        return jsonify({'status': 'new message', 'message': message})

    else:
        return jsonify({'status': 'Error', 'message': 'Client not found'})

# Route for sending messages back to the client
@app.route('/spectator', methods=['GET'])
def spectator():
    client_ip = request.remote_addr

    # Find the client instance, and make sure its valid
    client = None
    for c in game.get_spectators():
        if c.ip == client_ip:
            client = c
            break
    if not client:
        return jsonify({'status': 'Error', 'message': 'Client not found'})
    if (len(game.get_messages()) > 0):
        message = game.get_messages()
    else:
        message = ''

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

import network
import urequests
import ujson
import time


'''wifi'''
def connWIFI(WIFI_SSID,WIFI_PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WIFI_SSID,WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Connected to Network")
    #return IP address
    return wlan.ifconfig()[0]

'''helper functions for server connection'''
def translate_toUCI(move):    
    UCImove = ''
    # temp until we figure out castle on board
    castle_flag = 0
    
    if castle_flag == 1:
        if move == '5 7':
            UCImove = 'e1h1 '
        elif move == '5 3':
            UCImove = 'e1a1 '
        elif move == '61 63':
            UCImove = 'e8h8 '
        elif move == '61 59':
            UCImove = 'e8a8 '
        castle_flag = 0
        return UCImove
    
    from_row = move[0][0] + 1
    from_col = chr(move[0][1] + 97)
    to_row = move[1][0] + 1
    to_col = chr(move[1][1] + 97)

    s1 = str(from_col)
    s2 = str(from_row)
    s3 = str(to_col)
    s4 = str(to_row)

    ##### Need to handle promotions somehow #####
    s5 = ' '

    UCImove = s1 + s2 + s3 + s4 + s5

    return UCImove

def translate_fromUCI(UCImove):
    move = ''

    # remove spaces
    UCImove = UCImove.replace(' ', '')

    ###update for castle###
    if UCImove == 'e1h1':
        move = '5 7'
        return move
    elif UCImove == 'e1a1':
        move = '5 3'
        return move
    elif UCImove == 'e8h8':
        move = '61 63'
        return move
    elif UCImove == 'e8a8':
        move = '61 59'
        return move

    from_row = int(UCImove[1]) - 1
    from_col = ord(UCImove[0]) - 96 -1
    to_row = int(UCImove[3]) -1 
    to_col = ord(UCImove[2]) - 96 -1


    move = ((abs(7-from_row),from_col),(abs(7-to_row),to_col))
    

    ##### Need to handle promotions somehow #####
    return move



class server:

    def __init__(self,SERVER_IP,SERVER_PORT):
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.spectator_msg = ''

    def connect(self):
        '''initial connection'''
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/'
        response = urequests.get(url)
        reply1 = response.text
        response.close()
        
        '''identify that this is a chessbaord'''
        data = {'message':'chessboard'}
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/identify'
        response = urequests.post(url, json=data)
        reply2 = response.text
        response.close()
        
        return str(reply1) + ' ' + str(reply2)
    
    def waiting_message(self):
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/waiting'
        response = urequests.get(url)
        reply = response.text
        response.close()
        #print(ujson.loads(reply))
        return ujson.loads(reply)['message'], ujson.loads(reply)['gametime']
    
    def waiting(self):
        print("waiting for game to start")
        playtype,gametime = self.waiting_message()
        #print(playtype,gametime)
        while ((playtype != 'white_player') and (playtype != 'black_player') and (playtype != 'spectator_player')):
            time.sleep(1)
            playtype,gametime = self.waiting_message()
        print("game has started")
        return playtype, gametime

    def send_move(self,message):
        '''send a move'''
        data = {'message':message}
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/sendmove'
        response = urequests.post(url, json=data)
        reply = response.text
        response.close()
        return reply
    
    def receive_move_message(self):
        '''check status(recive a move)'''
        start = time.time_ns()
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/receivemove'
        response = urequests.get(url)
        reply = response.text
        response.close()
        move = ujson.loads(reply)['message']
        end = time.time_ns()
        #print('Server Response time is: ' ,(end-start) / 1000000000.0, ' Seconds')
        
        #move = 'a1b1'
        return move
    
    def receive_move(self):
        recv = self.receive_move_message()
        while (recv == ''):
            recv = self.receive_move_message()
            time.sleep(1)
        return recv
    
    def spectator_message(self):
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/spectator'
        response = urequests.get(url)
        reply = response.text
        response.close()
        return ujson.loads(reply)['message']
    
    def spectator(self):
        spec = self.spectator_message()
        while spec == self.spectator_msg:
            spec = self.spectator_message()
            time.sleep(2)
        self.spectator_msg = spec
        return spec

        
    
if __name__ == "__main__":
    #connWIFI('CookeFamily','P@rty0fF!ve')
    
    # Basic code sends 1 message and gets 1 message
    connWIFI('Chickennuggs','13221322')
    
    server = server('192.168.84.30','5000')
    server.connect()
    playtype = server.waiting() # wait for game to start, returns what player type the micro is for this game
    print(playtype)
    
    while True:
        recv = server.spectator()
        print(recv)
        move = translate_fromUCI(recv[-1])
        print(move)


    '''
    server.connect()
    playtype = server.waiting() # wait for game to start, returns what player type the micro is for this game
    while True:
        move_str = input('Input move in form ((0, 3), (1, 3)): ')
        move = ((int(move_str[0]),int(move_str[1])),(int(move_str[2]),int(move_str[3])))
        print(move)
        uci = translate_toUCI(move)
        server.send_move(uci)
        time.sleep(5)
        recv = server.receive_move()
        move = translate_fromUCI(recv)
        print(move)
    '''
    
    #repeated move similar to a games logic
    '''
    connWIFI('Chickennuggs','13221322') #connect to wifi using this username and password
    server = server('192.168.140.30','5000') #connect to server at this ip and this port
    
    server.connect() # initializes connection with server, and identifies itself as the micro
    playtype = server.waiting() # wait for game to start, returns what player type the micro is for this game
    
    print(playtype)
    if playtype == 'white_player':   
        while True:
            move = input("Input a move:") #need to get move from hall effect sensors
            server.send_move(move) # returns what move the server recieved
            recv = server.receive_move() # This returns once a message from server is recived
            print("Move from the Server is: ",recv) #send motor movement to micah, and update board state?
    elif playtype == 'black_player':
        while True:
            recv = server.receive_move() # This returns once a message from server is recived
            print("Move from the Server is: ",recv) #send motor movement to micah, and update board state?
            move = input("Input a move:") #need to get move from hall effect sensors
            server.send_move(move) # returns what move the server recieved
    '''
    '''
    move = ((0, 3), (1, 3))
    uci = translate_toUCI(move)
    print(uci)
    move = translate_fromUCI(uci)
    print(move)
    '''
    
    
    
    
    
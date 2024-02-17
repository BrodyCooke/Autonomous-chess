import network
import urequests
import ujson
from machine import Timer
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

class server:

    def __init__(self,SERVER_IP,SERVER_PORT):
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT

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
    
    def waiting_message(self,Tim4):
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/waiting'
        response = urequests.get(url)
        reply = response.text
        response.close()
        self.waiting_message_content = ujson.loads(reply)['message']
    
    def waiting(self):
        print("waiting for game to start")
        playtype = ''
        while ((self.waiting_message() != 'white_player') and (self.waiting_message() != 'black_player')):
            time.sleep(1)
        playtype = self.waiting_message()
        print("game has started")
        return playtype

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
        print('Server Response time is: ' ,(end-start) / 1000000000.0, ' Seconds')
        return move
    
    def receive_move(self):
        recv = self.receive_move_message()
        while (recv == ''):
            recv = self.receive_move_message()
            time.sleep(1)
        return recv
        
    
if __name__ == "__main__":
    #connWIFI('CookeFamily','P@rty0fF!ve')
    '''
    # Basic code sends 1 message and gets 1 message
    connWIFI('Chickennuggs','13221322')
    
    server = server('192.168.188.30','5000')
    server.connect()
    time.sleep(5)
    server.send_move('12 28')
    time.sleep(5)
    print(server.receive_move())
    '''
    connWIFI('Chickennuggs','13221322') #connect to wifi using this username and password
    server = server('192.168.188.30','5000') #connect to server at this ip and this port
    
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
    while True:
        move = input("Input a move:")
        server.send_move(move)
        recv = server.apicall()
        print(recv)
        '''
    
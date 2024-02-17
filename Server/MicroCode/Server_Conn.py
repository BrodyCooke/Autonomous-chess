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
        self.Tim4 = Timer(4)
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        self.waiting_message_content = ''
        self.receive_message_content = ''

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
        self.Tim4.init(mode=Timer.PERIODIC, period= 1000, callback=self.waiting_message)
        print("waiting for game to start")
        playtype = ''
        while ((self.waiting_message_content != 'white_player') and (self.waiting_message_content != 'black_player')):
            time.sleep(1)
        self.Tim4.deinit()
        playtype = self.waiting_message_content
        self.waiting_message_content = ''
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
    
    def receive_move_message(self,Tim4):
        '''check status(recive a move)'''
        start = time.time()
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/receivemove'
        response = urequests.get(url)
        reply = response.text
        response.close()
        move = ujson.loads(reply)['message']
        end = time.time()
        #print('Server Response time is: ' ,end-start)
        self.receive_message_content = move
    
    def receive_move(self):
        self.Tim4.init(mode=Timer.PERIODIC, period= 1000, callback=self.receive_move_message)
        while (self.receive_message_content == ''):
            time.sleep(1)
        self.Tim4.deinit()
        rtv = self.receive_message_content
        self.receive_message_content = ''
        return rtv
        
    
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
    connWIFI('Chickennuggs','13221322')
    server = server('192.168.188.30','5000')
    
    server.connect()
    playtype = server.waiting()
    
    print(playtype)
    if playtype == 'white_player':   
        while True:
            move = input("Input a move:")
            server.send_move(move)
            recv = server.receive_move()
            print("Move from the Server is: ",recv)
    elif playtype == 'black_player':
        while True:
            recv = server.receive_move()
            print("Move from the Server is: ",recv)
            move = input("Input a move:")
            server.send_move(move)
        
    '''
    while True:
        move = input("Input a move:")
        server.send_move(move)
        recv = server.apicall()
        print(recv)
        '''
    
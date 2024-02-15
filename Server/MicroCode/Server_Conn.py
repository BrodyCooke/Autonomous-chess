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

class server:

    def __init__(self,SERVER_IP,SERVER_PORT):
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT

    def connect(self):
        '''initial connection'''
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/'
        response = urequests.get(url)
        reply = response.text
        response.close()
        return reply

    def send_move(self,message):
        '''send a move'''
        data = {'message':message}
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/sendmove'
        response = urequests.post(url, json=data)
        reply = response.text
        response.close()
        return reply
    
    def receive_move(self):
        '''check status(recive a move)'''
        start = time.time()
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/receivemove'
        response = urequests.get(url)
        reply = response.text
        response.close()
        move = ujson.loads(reply)['message']
        end = time.time()
        print('Server Response time is: ' ,end-start)
        return move
    
if __name__ == "__main__":
    #connWIFI('CookeFamily','P@rty0fF!ve')
    '''
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
    while True:
        move = input("Input a move:")
        server.send_move(move)
        recv = server.receive_move()
        while (recv == ''):
            recv = server.receive_move()
            time.sleep(.5)
        print(recv)
    
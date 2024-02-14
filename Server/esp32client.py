import network
import urequests


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

    def send_move(self,data):
        '''send a move'''
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/sendmove'
        response = urequests.post(url, json=data)
        reply = response.text
        response.close()
        return reply
    
    def receive_move(self):
        '''check status(recive a move)'''
        url = 'http://' + self.SERVER_IP + ':' + self.SERVER_PORT + '/receivemove'
        response = urequests.get(url)
        reply = response.text
        response.close()
        return reply
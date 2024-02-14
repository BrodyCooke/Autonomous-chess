class Client:
    def __init__(self, ip):
        self.ip = ip
        self.message_history = []
        self.lastmessage = ''
        self.source = ''
        self.pair = None

    def add_message(self, message):
        self.message_history.append(message)
        self.lastmessage = message
    
    def get_messages(self):
        return self.message_history
    
    def get_lastmessage(self):
        return self.lastmessage
    
    def zero_lastmessage(self):
        self.lastmessage = ''

    def set_pair(self, _pair):
        self.pair = _pair

    def get_pair(self):
        return self.pair
    
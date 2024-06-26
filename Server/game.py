class Game:
    def __init__(self):
        self.message_history = []
        self.lastmessage = 'started'
        self.p_white = None
        self.p_black = None
        self.spectators = []
        self.clients = []
        self.endgame = 0
        self.gametime = 0

    def add_message(self, message):
        self.message_history.append(message)
        self.lastmessage = message
    
    def get_messages(self):
        return self.message_history
    
    def set_lastmessage(self, message):
        self.lastmessage = message
         
    def get_lastmessage(self):
        return self.lastmessage
    
    def zero_lastmessage(self):
        self.lastmessage = ''

    def set_white(self,client):
        self.p_white = client

    def get_white(self):
        return self.p_white
    
    def set_black(self,client):
        self.p_black = client
        
    def get_black(self):
        return self.p_black
    
    def add_spectator(self,client):
        self.spectators.append(client)

    def get_spectators(self):
        return self.spectators
    
    def add_client(self,client):
        self.clients.append(client)
    
    def get_clients(self):
        return self.clients
    
    def set_endgame(self,val):
        self.endgame == val

    def is_endgame(self):
        return self.endgame
    
    def set_gametime(self,gametime):
        self.gametime= gametime

    def get_gametime(self):
        return self.gametime
    

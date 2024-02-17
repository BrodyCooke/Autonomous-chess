class Client:
    def __init__(self, ip):
        self.ip = ip
        self.type = ''
        self.color = '' #includes spectator
        self.previousmove = ''

    def set_type(self, identity):
        self.type = identity

    def get_type(self):
        return self.type
    
    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color
    
    def set_previousmove(self, move):
        self.previousmove = move
    
    def get_previousmove(self):
        return self.previousmove
    
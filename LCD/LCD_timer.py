import machine
from machine import Pin, SoftI2C, Timer
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

class LCD_timer:
    def __init__(self, player_time):
        self.untimed_mode 		= False # if true change p1/p2 to count up.
        self.p1_sec 			= 0
        self.p1_min 			= int(player_time)
        self.p2_sec 			= 0
        self.p2_min 			= int(player_time)
        self.player_turn 		= 1
        self.string_p1 			= str(self.p1_min) + ":" + self.zero_sec
        self.string_p2 			= str(self.p2_min) + ":" + self.zero_sec
        self.string_comb 		= self.string_p1 + "     " + self.string_p2
        self.zero_sec 			= "00"
        self.I2C_ADDR 			= 0x27
        self.totalRows 			= 2
        self.totalColumns 		= 16
        
        self.i2c 				= SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
        self.lcd 				= I2cLcd(self.i2c, self.I2C_ADDR, self.totalRows, self.totalColumns)
        self.tim0 				= Timer(0)
        self.paused 			= True
        
        self.lcd.putstr("Player1  Player2")
        
        self.tim0.init(mode=Timer.PERIODIC, period=1*1000, callback=self.countdown)
        
# def button_press(pin):
#     
#     count = 0
#     
#     prevval = pir.value()
#     ##check to make sure the button is the same 10 times in a row,  ie bouncing is likely done
#     while count <10:
#         if pir.value() == prevval:   #button was the same as previous, increment count
#             count = count + 1
#             prevval = pir.value()
#         else:                           #button was not the same reset the count
#             count = 0
#     #now that bouncing is done if we still have a value of 0 update the mode    
#     lcd.clear()
#     lcd.move_to(0,1)
#     lcd.putstr("7:00")
#     while(turn ==0)
#         lcd.clear()
#         lcd.move_to(0,1)
#         str_time = t_min + ":" + t_secs
#         lcd.putstr(str_time)
#     sleep(5)
#     lcd.clear()
#         

    def countdown(self):
        if not self.paused: 
            if self.player_turn == 1:
                self.p1_sec = self.p1_sec - 1
                
                if self.p1_sec < 0:
                    self.p1_sec = 59
                    self.p1_min = self.p1_min - 1
                
                if self.p1_min <0:
                    # print("Stop Game")
                    self.lcd.clear()
                    self.lcd.putstr("Game Over")
                    self.tim0.deinit()
                    
                if self.p1_sec == 0:
                    self.string_p1 = str(self.p1_min) + ":" + self.zero_sec
                elif self.p1_sec < 10:
                    self.string_p1 = str(self.p1_min) + ":0" + str(self.p1_sec)
                else:
                    self.string_p1 = str(self.p1_min) + ":" + str(self.p1_sec)
                
                #string_p1 = str(p1_min) + ":"+ str(p1_sec)
                
            if self.player_turn == 2:
                self.p2_sec = self.p2_sec - 1
                
                if self.p2_sec < 0:
                    self.p2_sec = 59
                    self.p2_min = self.p2_min - 1
                
                if self.p2_min <0:
                    # print("Stop Game")
                    self.lcd.clear()
                    self.lcd.putstr("Game Over")
                    self.tim0.deinit()
                if self.p2_sec == 0:
                    self.string_p2 = str(self.p2_min) + ":"+ self.zero_sec
                elif self.p2_sec < 10:
                    self.string_p2 = str(self.p2_min) + ":0" + str(self.p2_sec)
                else:
                    self.string_p2 = str(self.p2_min) + ":"+ str(self.p2_sec)
            
        
        self.lcd.move_to(0,1)
        self.string_comb = self.string_p1 + "     " + self.string_p2
        self.lcd.putstr(self.string_comb)
    
    def pause(t):
        self.paused = True
        
    def unpause(self):
        if self.player_turn == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1
        self.paused = False
        
# Set-up a timer to constantly run for every second to count down using periodic.
    #def initialize(player_time):
        #player_time = int(player_time)
        #I2C_ADDR = 0x27
        #totalRows = 2
        #totalColumns = 16
        
        

        #p1_sec = 00
        #p1_min = player_time
        #p2_sec = 00
        #p2_min = player_time
        #zero_sec = str("00")
        #if p1_sec == 0:
            
        #    string_p1 = str(p1_min) + ":"+ zero_sec
        #else:
        #    string_p1 = str(p1_min) + ":"+ str(p1_sec)
        #if p2_sec == 0:
        #    string_p2 = str(p2_min) + ":"+ zero_sec
        #else:
        #    string_p2 = str(p2_min) + ":"+ str(p2_sec)
        #string_p2 = str(p2_min) + ":"+ str(p2_sec)
        #string_comb =string_p1 + "     " + string_p2

        
        #player_turn =1
        #speed = Pin(13,Pin.OUT)
        #speed.value(0)
        #i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)     #initializing the I2C method for ESP32 (sda 22, scl 14)
        
        #lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
        #lcd.putstr("Player1  Player2")
        #tim0 = Timer(0)
        #pir = Pin(34,Pin.IN)
        #pir.irq(trigger=Pin.IRQ_RISING, handler=pause)
    

if __name__ == "__main__":
    x = input("Input Play Time 1:9: ")
    
    #initialize(x)
    
#     Scan (Done)
#     On Button:
#         Scan
#         check valid move
#             turn on red light
#             wait for button hit
#         translate move (start Timer for API)
#         send move 
#         receive move (api)
#         translate move(stop Timer for API)
#         move piece (this updates all variables)
#         Start Player timer (Wait for player button press)
        
        
        


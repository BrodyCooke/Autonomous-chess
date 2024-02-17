import machine
from machine import Pin, SoftI2C, Timer
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

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

def countdown(t):
    global p1_sec
    global p1_min
    global p2_sec
    global p2_min
    global player_turn
    global string_p1
    global string_p2
    global string_comb
    global zero_sec
    global lcd
    if player_turn == 1:
        p1_sec = p1_sec - 1
        
        if p1_sec < 0:
            p1_sec = 59
            p1_min = p1_min - 1
        
        if p1_min <0:
            print("Stop Game")
            lcd.clear()
            lcd.putstr("Game Over")
            tim0.deinit()
            
        if p1_sec == 0:
            string_p1 = str(p1_min) + ":"+ zero_sec
        else:
            string_p1 = str(p1_min) + ":"+ str(p1_sec)
        
        #string_p1 = str(p1_min) + ":"+ str(p1_sec)
        
    if player_turn == 2:
        p2_sec=p2_sec - 1
        
        if p2_sec < 0:
            p2_sec = 59
            p2_min = p2_min - 1
        
        if p2_min <0:
            print("Stop Game")
            lcd.clear()
            lcd.putstr("Game Over")
            tim0.deinit()
        if p2_sec == 0:
            string_p2 = str(p2_min) + ":"+ zero_sec
        else:
            string_p2 = str(p2_min) + ":"+ str(p2_sec)
        
    
    lcd.move_to(0,1)
    string_comb = string_p1 + "     " + string_p2
    lcd.putstr(string_comb)
    
def pause(t):
    global start_count
    #global speed
    global tim0
    start_count= start_count +1
    if start_count == 1:
        tim0.init(mode=Timer.PERIODIC, period=1*1000, callback=countdown)
    global player_turn
    #print("Button")
    #speed.value(1)
    if player_turn == 1:
        player_turn = 2
    else:
        player_turn = 1

# Set-up a timer to constantly run for every second to count down using periodic.
def initialize(player_time):
    #global speed
    global player_turn
    global tim0
    global p1_sec
    global p1_min
    global p2_sec
    global p2_min
    global player_turn
    global string_p1
    global string_p2
    global string_comb
    global zero_sec
    global lcd
    global start_count
    player_time = int(player_time)
    I2C_ADDR = 0x27
    totalRows = 2
    totalColumns = 16
    
    start_count = 0

    p1_sec = 00
    p1_min = player_time
    p2_sec = 00
    p2_min = player_time
    zero_sec = str("00")
    if p1_sec == 0:
        
        string_p1 = str(p1_min) + ":"+ zero_sec
    else:
        string_p1 = str(p1_min) + ":"+ str(p1_sec)
    if p2_sec == 0:
        string_p2 = str(p2_min) + ":"+ zero_sec
    else:
        string_p2 = str(p2_min) + ":"+ str(p2_sec)
    #string_p2 = str(p2_min) + ":"+ str(p2_sec)
    string_comb =string_p1 + "     " + string_p2

    pir = Pin(34,Pin.IN)
    player_turn =1
    #speed = Pin(13,Pin.OUT)
    #speed.value(0)
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)     #initializing the I2C method for ESP32 (sda 22, scl 14)
    #i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)       #initializing the I2C method for ESP8266
    lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
    lcd.putstr("Player1  Player2")
    tim0 = Timer(0)
    
    pir.irq(trigger=Pin.IRQ_RISING, handler=pause)
    

if __name__ == "__main__":
    
    
    x = input("Input Play Time 1:9: ")
    
    initialize(x)


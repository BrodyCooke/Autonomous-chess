from machine import ADC, Pin, Timer
import time

'''
adc_pin = Pin(14)
adc = ADC(adc_pin)

gpio_pin1 = Pin(32, Pin.OUT)
gpio_pin2 = Pin(27, Pin.OUT)
gpio_pin3 = Pin(13, Pin.OUT)'''

adc_pin = Pin(35)
adc = ADC(adc_pin)


gpio_pin1 = Pin(5, Pin.OUT)
gpio_pin2 = Pin(4, Pin.OUT)
gpio_pin3 = Pin(2, Pin.OUT)
gpio_pin4 = Pin(13, Pin.OUT)
gpio_pin5 = Pin(14, Pin.OUT)
gpio_pin6 = Pin(17, Pin.OUT)

States =[[1,1,1],[1,0,1],[0,1,1],[0,0,1],[0,1,0],[1,0,0],[0,0,0],[1,1,0]]
New_States = [[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]]

def reset(t):
    analog_value = adc.read()
    print("Analog Value:", analog_value)
    #gpio_pin1.value(gpio_pin1.value()^1)
    #gpio_pin2.value(gpio_pin2.value()^1)
    #gpio_pin3.value(gpio_pin3.value()^1)

#tim0 = Timer(0)
#tim0.init(mode=Timer.PERIODIC, period=2*1000, callback=reset)

def read_halleffects_cont():
    while True:
        for x in States:
            gpio_pin1.value(x[2])
            gpio_pin2.value(x[1])
            gpio_pin3.value(x[0])
            time.sleep(.5)
            analog_value = adc.read()
            if analog_value < 3000:
                print(analog_value)
                #return x
                #break

def read_halleffects_once():
    values = []
    temp_list = []
    for i in New_States:
        gpio_pin4.value(i[2])
        gpio_pin5.value(i[1])
        gpio_pin6.value(i[0])
        temp_list = []
        for x in States:
            gpio_pin1.value(x[2])
            gpio_pin2.value(x[1])
            gpio_pin3.value(x[0])
            #time.sleep(.025)
            time.sleep(.3)
            analog_value = adc.read()
            print(analog_value)
            if analog_value > 2200:
                temp_list.append(1)
            elif analog_value < 1800:
                temp_list.append(-1)
            else:
                temp_list.append(0)
        values.append(temp_list)    
            
    printlist(values)
    return values

def printlist (final_list):
    for value in final_list:
        print (value)
    
        
def find_change():
    start = time.time_ns()
    first_values = read_halleffects_once()  # Get the initial array of values
    end = time.time_ns()
    print("Time to receive message from sensors: ",(end - start)/1000000000.0, " seconds")
    
    time.sleep(3)
    
    start = time.time_ns()
    while True:
        new_values = read_halleffects_once()  # Get a new array of values
        if new_values != first_values:  # Compare with the initial array
            print("Changes detected!")  # If there are differences, print a message
            print("First values:", first_values)
            print("New values:", new_values)
        else:
            print("Piece Location:", first_values)
        break
    
    end = time.time_ns()
    print("Time to receive message from sensors: ",(end - start)/1000000000.0, " seconds")
    '''while True:
        print(read_halleffects_cont())
        time.sleep(.5)
    print(read_halleffects_once())'''
    return new_values
    
if __name__ == '__main__':
    #find_change()
    
    read_halleffects_once()
    '''
    gpio_pin4.value(0)
    gpio_pin5.value(0)
    gpio_pin6.value(1)
    gpio_pin1.value(0)
    gpio_pin2.value(0)
    gpio_pin3.value(0)
    
    for x in States:
        gpio_pin1.value(x[2])
        gpio_pin2.value(x[1])
        gpio_pin3.value(x[0])
        time.sleep(.5)
        analog_value = adc.read()
        print(analog_value)
    '''
    '''
    
    
    gpio_pin1.value(1)
    gpio_pin2.value(1)
    gpio_pin3.value(1)
    while True:
        time.sleep(.5)
        analog_value = adc.read()
        print(analog_value)
        '''

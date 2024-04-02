from machine import ADC, Pin, Timer
import time

'''
adc_pin = Pin(14)
adc = ADC(adc_pin)

gpio_pin1 = Pin(32, Pin.OUT)
gpio_pin2 = Pin(27, Pin.OUT)
gpio_pin3 = Pin(13, Pin.OUT)'''

adc_pin = Pin(36)
adc = ADC(adc_pin)


gpio_pin1 = Pin(14, Pin.OUT)
gpio_pin2 = Pin(32, Pin.OUT)
gpio_pin3 = Pin(15, Pin.OUT)

States =[[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]]

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
            gpio_pin1.value(x[0])
            gpio_pin2.value(x[1])
            gpio_pin3.value(x[2])
            time.sleep(.5)
            analog_value = adc.read()
            if analog_value < 3000:
                print(analog_value)
                #return x
                #break

def read_halleffects_once():
    values = []
    for x in States:
        gpio_pin1.value(x[0])
        gpio_pin2.value(x[1])
        gpio_pin3.value(x[2])
        #time.sleep(.025)
        time.sleep(.5)
        analog_value = adc.read()
        print(analog_value)
        if analog_value > 2000:
            values.append(1)
        elif analog_value < 1500:
            values.append(-1)
        else:
            values.append(0)
    return values
        
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
    
    
    gpio_pin1.value(0)
    gpio_pin2.value(0)
    gpio_pin3.value(0)
    while True:
        time.sleep(.5)
        analog_value = adc.read()
        print(analog_value)

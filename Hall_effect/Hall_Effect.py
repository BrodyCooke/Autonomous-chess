from machine import ADC, Pin, Timer
import time

adcpin = Pin(14)
adc = ADC(adcpin)
# need to update the pins for wroom
gpiopin1 = Pin(32, Pin.OUT)
gpiopin2 = Pin(27, Pin.OUT)
gpio_pin3 = Pin(13, Pin.OUT)

States =[[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1]]

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
            time.sleep(.05)
            analog_value = adc.read()
            if analog_value < 3000:
                print(analog_value)
                return x
                #break

def read_halleffects_once():
    values = []
    for x in States:
        gpio_pin1.value(x[0])
        gpio_pin2.value(x[1])
        gpio_pin3.value(x[2])
        time.sleep(.05)
        analog_value = adc.read()
        if analog_value < 3000:
            values.append(1)
        else:
            values.append(0)
    return values

if __name == '__main':
    '''while True:
        print(read_halleffects_cont())
        time.sleep(.5)'''
    print(read_halleffects_once())
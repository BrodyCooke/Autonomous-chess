from machine import Pin, PWM
import time

#Define H-bridge control pins
#pin1 = Pin(1, Pin.OUT)  # Replace with your GPIO pin numbers
pin1= Pin(19,Pin.OUT)
pin2 = Pin(2, Pin.OUT)


# Define the GPIO pins for the H-bridge inputs
IN1 = Pin(15, Pin.OUT)   # Replace 5 with your actual GPIO pin number
IN2 = Pin(16, Pin.OUT)   # Replace 4 with your actual GPIO pin number
IN3 = Pin(23, Pin.OUT)   # Replace 0 with your actual GPIO pin number
IN4 = Pin(25, Pin.OUT)   # Replace 2 with your actual GPIO pin number
IN5 = Pin(26, Pin.OUT)   # Replace 5 with your actual GPIO pin number
IN6 = Pin(27, Pin.OUT)   # Replace 4 with your actual GPIO pin number
IN7 = Pin(32, Pin.OUT)   # Replace 0 with your actual GPIO pin number
IN8 = Pin(33, Pin.OUT)   # Replace 2 with your actual GPIO pin number
# Define steps for one revolution (200 for a 1.8 degree per step motor)
STEPS_PER_REVOLUTION = 100


# Function to set the H-bridge state using PWM
def set_stepx(w1, w2, w3, w4):
    IN1.value(w1)
    IN2.value(w2)
    IN3.value(w3)
    IN4.value(w4)

def set_stepy(w5, w6, w7, w8):
    IN5.value(w5)
    IN6.value(w6)
    IN7.value(w7)
    IN8.value(w8)
# Function to make one step
def step(motor, delay):
    if motor == "x":
        #print("x")
        set_stepx(1,0,1,0)
        time.sleep_ms(delay)
        set_stepx(0,1,1,0)
        time.sleep_ms(delay)
        set_stepx(0,1,0,1)
        time.sleep_ms(delay)
        set_stepx(1,0,0,1)
        time.sleep_ms(delay)
    else:
        #print("y")
        set_stepy(1,0,1,0)
        time.sleep_ms(delay)
        set_stepy(0,1,1,0)
        time.sleep_ms(delay)
        set_stepy(0,1,0,1)
        time.sleep_ms(delay)
        set_stepy(1,0,0,1)
        time.sleep_ms(delay)
# Function to rotate the motor a specified number of steps
def rotate(motor, steps, delay=10):
    for _ in range(abs(steps)):
        if steps > 0:
            step(motor, delay)
        if steps < 0:
            reverse_step_sequence(motor, delay)
        


# Function to reverse the step sequence for changing direction
def reverse_step_sequence(motor, delay):
    
    if motor == "x":
        set_stepx(1,0,0,1)
        time.sleep_ms(delay)
        set_stepx(0,1,0,1)
        time.sleep_ms(delay)
        set_stepx(0,1,1,0)
        time.sleep_ms(delay)
        set_stepx(1,0,1,0)
        time.sleep_ms(delay)
    else:
        set_stepy(1,0,0,1)
        time.sleep_ms(delay)
        set_stepy(0,1,0,1)
        time.sleep_ms(delay)
        set_stepy(0,1,1,0)
        time.sleep_ms(delay)
        set_stepy(1,0,1,0)
        time.sleep_ms(delay)


# Function to activate electromagnet
def activate_electromagnet():
    pin1.value(1)
    pin2.value(0)

#Function to deactivate electromagnet
def deactivate_electromagnet():
    pin1.value(0)
    pin2.value(0)

# Function to reverse polarity
def reverse_polarity():
    pin1.value(0)
    pin2.value(1)

# Example usage
if __name__ == "__main__":
    print("Activate E-Mag")
    activate_electromagnet()
    print("Motor Start")
    # Example usage
    rotate("y", 825, 6)  # Rotate 200 steps (one revolution) at a faster speed
    print("24 Volt Motor Start")
    rotate("x", -400, 13)  # Rotate 200 steps (one revolution) at a faster speed

    deactivate_electromagnet()



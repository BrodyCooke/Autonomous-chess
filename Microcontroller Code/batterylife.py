from machine import ADC, Pin, Timer, SoftI2C
import time
import pcf8575

def battery_check(adc,pcf):
    battery_life = (adc.read() / 4095)
    if battery_life < 0.76:
        pcf.pin(3,1)
    else:
        pcf.pin(3,0)
    print(battery_life)
    
if __name__ == "__main__":
    adc_pin = Pin(32)
    adc = ADC(adc_pin)
    print("ADC read")

    i2c_set = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
    pcf = pcf8575.PCF8575(i2c_set, 0x20)
    while True:
        battery_check(adc,pcf)
        time.sleep(3)

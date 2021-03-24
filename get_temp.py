import machine
from utime import sleep
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

def get_temperature():
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = round(27 - (reading - 0.706)/0.001721, 2)
    
    return "Temp "+str(temperature)+"C"
    
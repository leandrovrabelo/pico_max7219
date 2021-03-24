from max7219 import Matrix8x8
from machine import Pin, SPI
from utime import sleep

if __name__ == '__main__':
    CS = Pin(5, Pin.OUT) # GPIO5 pin 7
    CLK = Pin(6) # GPIO6 pin 9
    DIN = Pin(7) # GPIO7 pin 10
    BRIGHTNESS = 3 # from 0 to 15
    
    text1 = "Hello World!"
    text2 = "PICO PI"
    # CLK = GPIO6 and MOSI (DIN) = GPIO6 are the default pins of SPI0 so you can omit it
    spi = SPI(0, baudrate= 10_000_000,  sck=CLK, mosi=DIN)
    display = Matrix8x8(spi, CS, 1, orientation=1)
    display.brightness(BRIGHTNESS)
    display.invert = False
    
    while True:
        
        # all on
        display.fill(True)
        display.show()
        sleep(0.5)

        # all off
        display.fill(False)
        display.show()
        sleep(0.5)

        # show a string scrolling through the Matrix
        display.text_scroll(text1)
        
        # show a string one character at a time
        display.one_char_a_time(text2, delay=0.25)
        
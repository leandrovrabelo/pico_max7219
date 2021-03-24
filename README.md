# Raspberry Pico MAX7219 Matrix LED
An Pico integration to [FideliusFalcon' MicroPython MAX7219 library](https://github.com/FideliusFalcon/rpi_pico_max7219) and also some parts from [Adafruit's Circuit Python Max7219](https://github.com/adafruit/Adafruit_CircuitPython_MAX7219).


## Wiring
The Pico does'nt have a 5v pin, but the VBUS is connected to the power input. The MAX7219 need an 5v input, so the Pico's power supply will have to be 5v. This is the default pins for SPI0.
|MAX7219|Pico Name|Pico GPIO|Pico PIN|
|-|-|-|-|
|VCC|VBUS||40|
|GND|GND||38|
|DIN|MOSI (SPI0 TX)|GP7|10|
|CS|SPI0 CSn|GP5|7|
|CLK|SCK|GP6|9|

Usage Example
=============

.. code:: python

  from max7219 import Matrix8x8
  from machine import Pin, SPI
  from utime import sleep
  from get_temp import get_temperature
  
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

      # show a string scrolling through the Matrix
      display.text_scroll(text1)

      # Get temperature from sensor on Pico
      temp = get_temperature()
      display.text_scroll(temp)
      
      # show a string one character at a time
      display.one_char_a_time(text2)
        
from micropython import const
import framebuf
from utime import sleep

_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

class Matrix8x8:
    def __init__(self, spi, cs, num, orientation=0):
        """
        CS = Pin(5, Pin.OUT) # GPIO5 pin 7
        CLK = Pin(6) # GPIO6 pin 9
        DIN = Pin(7) # GPIO7 pin 10
        BRIGHTNESS = 3 # from 0 to 15
        
        text = "Hello World!"
        # CLK = GPIO6 and MOSI (DIN) = GPIO6 are the default pins of SPI0 so you can omit it
        spi = SPI(0, baudrate= 10_000_000,  sck=CLK, mosi=DIN)
        display = Matrix8x8(spi, CS, 1, orientation=1)
        display.brightness(BRIGHTNESS)
        display.invert = False

        """
        ORIENTATION_CONST = [framebuf.MONO_VLSB, # Vertical
                             framebuf.MONO_HLSB, # Horizontal
                             framebuf.MONO_HMSB] # Horizontal Mirror
        
        self.orientation = ORIENTATION_CONST[orientation]
        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(8 * num)
        self.num = num
        fb = framebuf.FrameBuffer(self.buffer, 8 * num, 8, self.orientation)
        self.framebuf = fb
        # Provide methods for accessing FrameBuffer graphics primitives. This is a workround
        # because inheritance from a native class is currently unsupported.
        # http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
        self.fill = fb.fill  # (col)
        self.pixel = fb.pixel # (x, y[, c])
        self.hline = fb.hline  # (x, y, w, col)
        self.vline = fb.vline  # (x, y, h, col)
        self.line = fb.line  # (x1, y1, x2, y2, col)
        self.rect = fb.rect  # (x, y, w, h, col)
        self.fill_rect = fb.fill_rect  # (x, y, w, h, col)
        self.text = fb.text  # (string, x, y, col=1)
        self.scroll = fb.scroll  # (dx, dy)
        self.blit = fb.blit  # (fbuf, x, y[, key])
        self.invert = False
        self.init()

    def _write(self, command, data):
        self.cs(0)
        for m in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    def show(self):
        for y in range(8):
            self.cs(0)
            for m in range(self.num):
                self.spi.write(bytearray([_DIGIT0 + y, self.buffer[(y * self.num) + m]]))
            self.cs(1)

    def text_scroll(self, text, delay=0.1):

        text_lenght = len(text) * 8
        for pixel_position in range(text_lenght):
            self.fill(self.invert)
            self.text(text, -pixel_position, 0, not self.invert)
            self.show()
            sleep(delay)

    def one_char_a_time(self, text, delay=0.2):
        # show a string one character at a time

        for char in text:
            self.fill(self.invert)
            self.text(char, 0, 0, not self.invert)
            self.show()
            sleep(delay)
            
        # scroll the last character off the display          
        for i in range(8):
            self.scroll(-1, 0)
            self.show()
            sleep(delay)
        
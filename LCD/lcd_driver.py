import io

class LCDDriver(object):
    def __init__(self, spi_interface):
        self._spi = spi_interface
        self.width = 240
        self.height = 320 

    def command(self, command: bytes):
        self._spi.send_command(command)

    def data(self, data: bytes):
        self._spi.send_command(data)

    def set_draw_window(self, Xstart, Ystart, Xend, Yend):
        #set the X coordinates
        self.command(b'\x2A')

        self.data(Xstart.to_bytes(2, 'big')) 
        self.data((Xend - 1).to_bytes(2, 'big')) 

        #self.data(Xstart.to_bytes(2, 'big')[::-1]) 
        #self.data((Xend - 1).to_bytes(2, 'big')[::-1]) 

        #self.command(0x2A)
        #self.data(Xstart>>8)        #Set the horizontal starting point to the high octet
        #self.data(Xstart & 0xff)    #Set the horizontal starting point to the low octet
        #self.data(Xend>>8)          #Set the horizontal end to the high octet
        #self.data((Xend - 1) & 0xff)#Set the horizontal end to the low octet 

        #set the Y coordinates
        self.command(b'\x2B')
        self.data(Ystart.to_bytes(2, 'big')) 
        self.data((Yend - 1).to_bytes(2, 'big')) 

        self.command(b'\x2C')

        #self.command(0x2B)
        #self.data(Ystart>>8)
        #self.data((Ystart & 0xff))
        #self.data(Yend>>8)
        #self.data((Yend - 1) & 0xff )

        #self.command(0x2C)   

    def fill_pixels(self, red: float, green: float, blue: float):
        r = int(red * 0b11111)
        g = int(green * 0b111111) << 5
        b = int(blue * 0b11111) << 11
        bt = (r|g|b).to_bytes(2, 'big')
        print(f"fill_pixels(red={red:0.2f}, green={green:0.2f}, blue={blue:0.2f}) - {bt}")
        self.fill((r|g|b).to_bytes(2, 'big'))
        

    def fill(self, pixel: bytes):
        """Fill image with a pixel"""
        stream = io.BytesIO(b'')

        for p in range(self.width * self.height):
            stream.write(pixel)

        self.set_draw_window ( 0, 0, self.height, self.width)
        #self.data(stream.getvalue())

        contents = stream.getvalue()
        # print(f"DEBUG 50bytes - {contents[:50]}")
        for i in range(0,len(contents),4096):
            self.data(contents[i:i+4096])	

    def clear(self):
        self.fill(b'\xFF\xFF')

        #pixels = [0xff]*(self.width * self.height * 2)
        #self.SetWindows ( 0, 0, self.height, self.width)
        #self.digital_write(self.DC_PIN,self.GPIO.HIGH)
        #for i in range(0,len(pixels),4096):
        #    self.spi_writebyte(pixels[i:i+4096])	


    def initialize(self):
        self._spi.reset()

        self.command(b'\x36')
        self.data(b'\x00') 
        self.command(b'\x3A') 
        self.data(b'\x05')
        self.command(b'\x21\x2A')
        self.data(b'\x00\x00\x01\x3F')
        self.command(b'\x2B')
        self.data(b'\x00\x00\x00\xEF')
        self.command(b'\xB2')
        self.data(b'\x0C\x0C\x00\x33\x33')
        self.command(b'\xB7')
        self.data(b'\x35') 
        self.command(b'\xBB')
        self.data(b'\x1F')
        self.command(b'\xC0')
        self.data(b'\x2C')
        self.command(b'\xC2')
        self.data(b'\x01')
        self.command(b'\xC3')
        self.data(b'\x12')   
        self.command(b'\xC4')
        self.data(b'\x20')
        self.command(b'\xC6')
        self.data(b'\x0F') 
        self.command(b'\xD0')
        self.data(b'\xA4\xA1')
        self.command(b'\xE0')
        self.data(b'\xD0\x08\x11\x08\x0C\x15\x39\x33\x50\x36\x13\x14\x29\x2D')
        self.command(b'\xE1')
        self.data( b'\xD0\x08\x10\x08\x06\x06\x39\x44\x51\x0B\x16\x14\x2F\x31')
        self.command(b'\x21\x11\x29')
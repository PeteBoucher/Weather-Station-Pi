from smbus import SMBus
import io

class HDC1008(object):
  """The temperature and Humidity sensor"""

  def __init__(self, bus_address = 0x40):
    self.addr = bus_address

  def get_temp(self):
    fr = io.open("/dev/i2c-"+str(1), "rb", buffering=0)
    fw = io.open("/dev/i2c-"+str(1), "wb", buffering=0)

    # set device address
    fcntl.ioctl(fr, I2C_SLAVE, self.addr)
    fcntl.ioctl(fw, I2C_SLAVE, self.addr)
    time.sleep(0.015) #15ms startup time

    s = [0x02,0x02,0x00]
    s2 = bytearray( s )
    fw.write( s2 ) #sending config register bytes
    time.sleep(0.015)               # From the data sheet

    s = [0x00] # temp
    s2 = bytearray( s )
    fw.write( s2 )
    time.sleep(0.0625)              # From the data sheet

    data = fr.read(2) #read 2 byte temperature data
    buf = array.array('B', data)
    return (((((buf[0]<<8) + (buf[1]))/65536.0)*165.0 ) - 40.0)

  def get_humid(self):
    pass

  def get_temp_and_humid(self):
    pass

  def get_heater(aelf):
    pass

  def set_heater(aelf, state):
    pass
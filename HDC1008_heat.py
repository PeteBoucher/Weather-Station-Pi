from smbus import SMBus
import struct, array, time, io, fcntl, json

HDC1008_ADDR = 0x40
I2C_SLAVE = 0x0703
CTRL_REG1 = 0x26
PT_DATA_CFG = 0x13
bus = SMBus(1)

def read_humidity(addr):
  bus=1
  fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
  fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

  # set device address
  fcntl.ioctl(fr, I2C_SLAVE, addr)
  fcntl.ioctl(fw, I2C_SLAVE, addr)
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
  # print ( "Temp: %f" % (  ((((buf[0]<<8) + (buf[1]))/65536.0)*165.0 ) - 40.0  )   )

  time.sleep(0.015)               # From the data sheet

  s = [0x01] # hum
  s2 = bytearray( s )
  fw.write( s2 )
  time.sleep(0.0625)              # From the data sheet

  data = fr.read(2) #read 2 byte temperature data
  buf = array.array('B', data)
  # return ( "Humidity: %f" % (  ((((buf[0]<<8) + (buf[1]))/65536.0)*100.0 ) ) )
  return ((((buf[0]<<8) + (buf[1]))/65536.0)*100.0 )

def read_temp(addr):
  fr = io.open("/dev/i2c-"+str(1), "rb", buffering=0)
  fw = io.open("/dev/i2c-"+str(1), "wb", buffering=0)

  # set device address
  fcntl.ioctl(fr, I2C_SLAVE, HDC1008_ADDR)
  fcntl.ioctl(fw, I2C_SLAVE, HDC1008_ADDR)
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

while True:
  humid = read_humidity(HDC1008_ADDR)
  print humid



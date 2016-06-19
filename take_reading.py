from smbus import SMBus
import RPi.GPIO as GPIO
import struct, array, time, io, fcntl, json, os, shelve

GPIO.setmode(GPIO.BCM)
HDC1008_ADDR = 0x40
MPL3115A2_ADDR = 0x60
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

def read_pressure(addr):
  # Enable event flags
  bus.write_byte_data(addr, PT_DATA_CFG, 0x07)

  # Toggel One Shot
  setting = bus.read_byte_data(addr, CTRL_REG1)
  if (setting & 0x02) == 0:
      bus.write_byte_data(addr, CTRL_REG1, (setting | 0x02))

  # Read sensor data
  # print "Waiting for data..."
    # Can throw an IOError
  status = 0b0
  while (status & 0x08) == 0:
    try:
      # Can throw an IOError
      status = bus.read_byte_data(addr,0x00)
    except Exception, e:
      pass
    time.sleep(0.5)
    # print "status: "+bin(status)

  # print "Reading sensor data..."
  # Can throw an IOError
  try:
    p_data = bus.read_i2c_block_data(addr,0x01,3)
    # t_data = bus.read_i2c_block_data(addr,0x04,2)
    status = bus.read_byte_data(addr,0x00)
    # print "status: "+bin(status)
  except Exception, e:
    raise e

  p_msb = p_data[0]
  p_csb = p_data[1]
  p_lsb = p_data[2]
  # t_msb = t_data[0]
  # t_lsb = t_data[1]

  pressure = (p_msb << 10) | (p_csb << 2) | (p_lsb >> 6)
  p_decimal = ((p_lsb & 0x30) >> 4)/4.0

  # celsius = t_msb + (t_lsb >> 4)/16.0
  # fahrenheit = (celsius * 9)/5 + 32

  # log_entry = "["+time.strftime('%Y%m%d %H:%M:%S%z')+"] temp:"+str(celsius)+" press:"+str((pressure+p_decimal)/100)
  # # print log_entry

  # with open('record.txt', 'a') as f:
  #   f.write(log_entry+"\n")

  # print "Pressure and Temperature at "+time.strftime('%d/%m/%Y %H:%M:%S%z')
  # print str((pressure+p_decimal)/100)+" mBar"
  # print str(celsius)+deg+"C"
  return ((pressure+p_decimal)/100)

anemometer_pin = 23
vane_pin = 24

def wind_speed(cups_pin, samples=1000000):
  GPIO.setup(cups_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  count = 0
  last_pulse = 0
  start_time = time.time()
  for i in range(samples):
    pulse = GPIO.input(cups_pin)
    if (pulse == 1 and last_pulse == 0):
      count += 1
    last_pulse = pulse
  end_time = time.time()

  sample_duration = (end_time - start_time)

  # 1 rpm = 2 pulse/sec = 2.4 km/h wind speed
  return (count/sample_duration) * 2.4

humid = read_humidity(HDC1008_ADDR)
temp = read_temp(HDC1008_ADDR)
try:
  pressure = read_pressure(MPL3115A2_ADDR)
except Exception, e:
  pressure = 0
wind_speed = wind_speed(anemometer_pin, 10000000)

def log(temp,press,humid,wind):
  log_entry = "["+time.strftime('%Y%m%d %H:%M:%S%z')+"] temp:"+str(temp)+" press:"+str(pressure)+" humid:"+str(humid)+" wind_speed:"+str(wind["speed"])

  with open('/home/pi/record.txt', 'a') as f:
    f.write(log_entry+"\n")

def shelve(conditions):
  ws_path = os.path.dirname(os.path.abspath(__file__))
  log_file = ws_path+'webapp/record'
  with shelve.open(log_file) as data_store:
    key = time.strftime('%Y%m%d%H%M%S')

    data_store[key] = conditions

def store(conditions):
  shelve(conditions)
  record = {'datetime':time.strftime('%Y%m%d %H:%M:%S%z'),'conditions':conditions}
  with open('/home/pi/Weather-Station-Pi/webapp/record.json', 'a') as f:
    f.write(json.dumps(record)+"\n")


wind = {'speed':wind_speed,'direction':0}

log(temp,pressure,humid,wind)

conditions = {'temp':temp,'press':pressure,'humid':humid,'wind':wind}

store(conditions)

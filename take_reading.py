from smbus import SMBus
import RPi.GPIO as GPIO
import struct, array, time, io, fcntl, json
import Adafruit_BMP.BMP085 as BMP180

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

def read_pressure():
  try:
    press_sensor = BMP180.BMP085()
  except IOError:
    pass
  return press_sensor.read_pressure()

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
  press_pascals = read_pressure()
  # Convert pascals to mBar
  pressure = float(press_pascals)/100
except Exception, e:
  pressure = 0.0

wind_speed = wind_speed(anemometer_pin, 10000000)

def log(temp,press,humid,wind):
  log_entry = "["+time.strftime('%Y%m%d %H:%M:%S%z')+"] temp:"+str(temp)+" press:"+str(pressure)+" humid:"+str(humid)+" wind_speed:"+str(wind["speed"])

  with open('/home/pi/record.txt', 'a') as f:
    f.write(log_entry+"\n")

def store(conditions):
  record = {'datetime':time.strftime('%Y%m%d %H:%M:%S%z'),'conditions':conditions}
  with open('/home/pi/Weather-Station-Pi/webapp/record.json', 'a') as f:
    f.write(json.dumps(record)+"\n")

wind = {'speed':wind_speed,'direction':0}

log(temp,pressure,humid,wind)

conditions = {'temp':temp,'press':pressure,'humid':humid,'wind':wind}

store(conditions)

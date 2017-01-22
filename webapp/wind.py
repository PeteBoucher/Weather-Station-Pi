import RPi.GPIO as GPIO, time
import Adafruit_MCP3008
GPIO.setmode(GPIO.BCM)

class Wind(object):

  def __init__(self, anemometer=17):
    self.anemometer_pin = anemometer
    adc_clk  = 18
    adc_miso = 23
    adc_mosi = 24
    adc_cs   = 25
    self.vane_mcp = Adafruit_MCP3008.MCP3008(clk=adc_clk, cs=adc_cs, miso=adc_miso, mosi=adc_mosi)

  def get_speed(self, unit='km/h'):
    rpm = self.speed(self.anemometer_pin)
    print 'anemometer RPM:', rpm
    # 1 rpm = 2.4 km/h wind speed
    if unit == 'km/h':
      speed = rpm * 2.4
    return speed

  def get_direction(self):
    # Read the signal from MCP3008 ch0 and calculate wind vane orientation
    signal = self.vane_mcp.read_adc(0) #wind vane is on ch0
    print "level:", signal
    directionSignals = [[0,930],[45,835],[90,730],[135,390],[180,75],[225,135],[270,235],[315,560]]

    direction = 'undefined'
    for d in directionSignals:
      if signal in range(d[1]-30, d[1]+30):
        direction = d[0]
        break

    return direction

  def speed(self, cups_pin, samples=1000000):
    GPIO.setup(cups_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    count = 0
    last_pulse = 0
    start_time = time.time() # unix timestamp
    for i in range(samples):
      pulse = GPIO.input(cups_pin)
      if (pulse == 1 and last_pulse == 0):
        count += 1
      last_pulse = pulse
    end_time = time.time() #Should use a real time clock for this as the raspi clock tends to drift

    duration_in_minutes = (end_time - start_time)/60

    # 1 revolution = 2 pulse
    revs = count/2
    return revs/duration_in_minutes

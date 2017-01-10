import RPi.GPIO as GPIO, time
GPIO.setmode(GPIO.BOARD)

class Wind(object):

  def __init__(self, anemometer=17, vane=5):
    self.anemometer_pin = anemometer
    self.vane_pin = vane

  def get_speed(self, unit='km/h'):
    rpm = self.speed(self.anemometer_pin)
    # 1 rpm = 2.4 km/h wind speed
    if unit == 'km/h':
      speed = rpm * 2.4
    return speed

  def get_direction(self):
    pass

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

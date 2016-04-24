import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
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
  return (count/sample_duration) * 1.2

def wind_direction(vane_pin):
  reading = 0
  GPIO.setup(vane_pin, GPIO.OUT)
  GPIO.setup(vane_pin, GPIO.LOW)
  time.sleep(0.1)

  GPIO.setup(vane_pin, GPIO.IN)
  while (GPIO.input(24) == GPIO.LOW):
    reading += 1
  return reading

def direction_res_to_deg(r):
  deg = 'out of range'
  if (135 < r < 235):
    deg = 0
  elif (365 < r < 465):
    deg = 45
  elif (710 < r < 810):
    deg = 90
  elif (3090 < r < 3190):
    deg = 135
  elif (12425 < r):
    deg = 180
  elif (12325 < r < 12425):
    deg = 225
  elif (6430 < r < 6530):
    deg = 270
  elif (1535 < r < 1635):
    deg = 315

  return deg

dir_res = wind_direction(vane_pin)
print 'Wind direction reding', dir_res
print 'Wind direction in degrees', direction_res_to_deg(dir_res)

print 'Wind speed in km/h', wind_speed(anemometer_pin)

GPIO.cleanup()

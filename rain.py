# Rain guage is connected to GPIO BCM22 and GND
import RPi.GPIO as GPIO
import time, json

rain_guage_pin = 22

def rainfall(guage_pin, samples = 1000000):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(guage_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

  count = 0
  start_time = time.time()
  for i in range(samples):
    pulse = GPIO.input(guage_pin)
    if (pulse == 0 and last_pulse == 1): #Circuit is closed to GND so a pulse = off
      count += 1
    last_pulse = pulse
  end_time = time.time()

  sample_duration = (end_time - start_time)

  return (count/sample_duration) * 0.2794

def log(rainfall):
  log_entry = "["+time.strftime('%Y%m%d %H:%M:%S%z')+"] rainfall:"+str(rainfall)

  with open('/home/pi/record.txt', 'a') as f:
    f.write(log_entry+"\n")

def store(rainfall):
  record = {'datetime':time.strftime('%Y%m%d %H:%M:%S%z'),'rainfall':rainfall}
  with open('/home/pi/Weather-Station-Pi/webapp/record.json', 'a') as f:
    f.write(json.dumps(record)+"\n")

while True:
  rain_mm = rainfall(rain_guage_pin)

  if rain_mm > 0:
    log(rain_mm)

    conditions = {'rainfall':rain_mm}
    store(conditions)

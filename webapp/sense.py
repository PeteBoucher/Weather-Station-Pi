import re, json, os
from datetime import datetime
from HDC1008 import HDC1008
import Adafruit_BMP.BMP085 as BMP180
from wind import Wind

class Sense(object):
  temp_sensor = HDC1008()
  try:
    press_sensor = BMP180.BMP085()
  except IOError:
    pass
  wind_sensor = Wind()

  """Access the weather station sensors"""
  def __init__(self):
    pass

  def read_log(self):
    with open('/home/pi/record.txt', 'r') as logfile:
      readings = logfile.readlines()
      return readings

  def log(self):
    with open('/home/pi/Weather-Station-Pi/webapp/record.json', 'r') as json_log:
      log = []
      for line in json_log:
        try:
          log.append(json.loads(line))
        except:
          pass
    return log

  def current_conditions(self):
    try:
      temp = self.temp_sensor.get_temp()
    except:
      temp = 'undefined'
    try:
      press = self.press_sensor.read_pressure()
    except:
      press = 'undefined'    
    wind_speed = self.wind_sensor.get_speed()
    wind_dir = self.wind_sensor.get_direction()

    history = self.log()

    # Direct access to these sensors is not implemented yet
    # read off the most recent log entry
    last_entry = history[-1:][0]
    try:
      press = last_entry['conditions']['press']
      humid = last_entry['conditions']['humid']
      wind_speed = last_entry['conditions']['wind']['speed']
    except:
      press = 'none'
      humid = 'none'
    time = last_entry['datetime']

    return [last_entry, temp, press, humid, time, wind_speed, wind_dir]

  def record_conditions(self):
    # {'temp':{'max':100,'min':0},'press':{},'humid':{}}
    temp = {'max':0, 'min':100}
    press = {'max':0, 'min':1500}
    humid = {'max':0, 'min':100}
    wind_speed = {'max':0, 'min':0}

    log = self.log()

    for record in log:
      if 'conditions' in record:
        if temp['max'] < record['conditions']['temp']:
          temp['max'] = record['conditions']['temp']
        if press['max'] < record['conditions']['press']:
          press['max'] = record['conditions']['press']
        if humid['max'] < record['conditions']['humid']:
          humid['max'] = record['conditions']['humid']
        if temp['min'] > record['conditions']['temp']:
          temp['min'] = record['conditions']['temp']
        if press['min'] > record['conditions']['press']:
          press['min'] = record['conditions']['press']
        if humid['min'] > record['conditions']['humid']:
          humid['min'] = record['conditions']['humid']
        if 'wind' in record['conditions']:
          record_wind = float(record['conditions']['wind']['speed'])
          if wind_speed['max'] < record_wind:
            wind_speed['max'] = record_wind
          if wind_speed['min'] > record_wind:
            wind_speed['min'] = record_wind

    return {'temp': temp, 'press': press, 'humid': humid, 'wind_speed': wind_speed}

  # Return CPU temperature as a character string
  def get_cpu_temp(self):
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

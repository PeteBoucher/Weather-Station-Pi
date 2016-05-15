import re, json
from datetime import datetime
from HDC1008 import HDC1008

class Sense(object):
  temp_sensor = HDC1008()

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
        log.append(json.loads(line))

    return log

  def current_conditions(self):
    temp = self.temp_sensor.get_temp()

    history = self.log()

    # Direct access to these sensors is not implemented yet
    # read off the most recent log entry
    last_entry = history[-1:][0]
    press = last_entry['conditions']['press']
    humid = last_entry['conditions']['humid']
    wind_speed = last_entry['conditions']['wind']['speed']
    time = last_entry['datetime']

    return [last_entry, temp, press, humid, time, wind_speed]

  def record_conditions(self):
    # {'temp':{'max':100,'min':0},'press':{},'humid':{}}
    temp = {'max':0, 'min':100}
    press = {'max':0, 'min':1500}
    humid = {'max':0, 'min':100}
    wind_speed = {'max':0, 'min':100}

    log = self.log()

    for record in log:
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
      if ('wind') in record['conditions']:
        if wind_speed['max'] > record['conditions']['wind']['speed']:
          wind_speed['max'] = record['conditions']['wind']['speed']
        if wind_speed['min'] > record['conditions']['wind']['speed']:
          wind_speed['min'] = record['conditions']['wind']['speed']

    return {'temp': temp, 'press': press, 'humid': humid, 'wind_speed': wind_speed}

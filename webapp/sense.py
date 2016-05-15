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

    last_entry = history[-1:][0]

    press = last_entry['conditions']['press']
    humid = last_entry['conditions']['humid']
    wind_speed = last_entry['conditions']['wind']['speed']
    time = last_entry['datetime']

    # with open('/home/pi/record.txt', 'r') as logfile:
    #   logfile.seek(-80, 2)
    #   last_entry = logfile.readlines()[-1]

    #   result = re.search('\[(?P<time>.*)\+0000\]', last_entry)
    #   timestamp = result.group('time')
    #   time = datetime.strptime(timestamp, "%Y%m%d %H:%M:%S")

    #   result = re.search('(?<=temp:)\d+\.\d+', last_entry)
    #   temp = float(result.group(0))

    #   result = re.search('(?<=humid:)\d+\.\d+', last_entry)
    #   humid = float(result.group(0))

    #   result = re.search('(?<=press:)\d+\.\d+', last_entry)
    #   press = float(result.group(0))
      # Sometimes the instrument reading script cannot get a value for press, go back to the last recoded pressure
      # while press==0:
      #   line = -2
      #   log = logfile.readlines()
      #   entry = log[line]
      #   result = re.search('(?<=press:)[\d+\.\d+|\d+]', entry)
      #   press = float(result.group(0))
      #   line = line-1

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
      if wind_speed['max'] > record['conditions']['wind']['speed']:
        wind_speed['max'] = record['conditions']['wind']['speed']
      if temp['min'] > record['conditions']['temp']:
        temp['min'] = record['conditions']['temp']
      if press['min'] > record['conditions']['press']:
        press['min'] = record['conditions']['press']
      if humid['min'] > record['conditions']['humid']:
        humid['min'] = record['conditions']['humid']
      if wind_speed['min'] > record['conditions']['wind']['speed']:
        wind_speed['min'] = record['conditions']['wind']['speed']

    return {'temp': temp, 'press': press, 'humid': humid, 'wind_speed': wind_speed}

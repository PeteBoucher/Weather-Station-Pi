import re
from datetime import datetime

class Sense(object):
  """Access the weather station sensors"""
  def __init__(self):
    pass

  def read_log(self):
    with open('/home/pi/record.txt', 'r') as logfile:
      readings = logfile.readlines()
      return readings

  def current_conditions(self):
    with open('/home/pi/record.txt', 'r') as logfile:
      logfile.seek(-80, 2)
      last_entry = logfile.readlines()[-1]

      result = re.search('\[(?P<time>.*)\+0000\]', last_entry)
      timestamp = result.group('time')
      time = datetime.strptime(timestamp, "%Y%m%d %H:%M:%S")

      result = re.search('(?<=temp:)\d+\.\d+', last_entry)
      temp = float(result.group(0))

      result = re.search('(?<=humid:)\d+\.\d+', last_entry)
      humid = float(result.group(0))

      result = re.search('(?<=press:)\d+\.\d+', last_entry)
      press = float(result.group(0))
      # Sometimes the instrument reading script cannot get a value for press, go back to the last recoded pressure
      # while press==0:
      #   line = -2
      #   log = logfile.readlines()
      #   entry = log[line]
      #   result = re.search('(?<=press:)[\d+\.\d+|\d+]', entry)
      #   press = float(result.group(0))
      #   line = line-1

      return [last_entry, temp, press, humid, time]
from sense import Sense

sensors = Sense()

print 'Pressure {0} Pa'.format(sensors.press_sensor.read_pressure())

log = sensors.read_log()
# print log

try:
  conditions = sensors.current_conditions()
  print 'Last sensor log entry:', conditions[0]

  print 'Temperature in deg C:', conditions[1]
  print 'Pressure in mBar:', conditions[2]
  print 'Relative Humidity:', conditions[3]
  print 'Last reading was taken at:', conditions[4]
  print 'Wind speed in km/h:', conditions[5]

except:
  print "Unable to get current_conditions check sensors are present"

print 'CPU temperature:', sensors.get_cpu_temp()

records = sensors.record_conditions()
print 'Record conditions:', records

print 'Min-Max temperature in deg C:', records['temp']['min'], records['temp']['max']
print 'Min-Max pressure in mBar:', records['press']['min'], records['press']['max']
print 'Min-Max relative Humidity:', records['humid']['min'], records['humid']['max']
print 'Min-Max wind speed in km/h:', records['wind_speed']['min'], records['wind_speed']['max']

day_log = sensors.conditions_on_date(date.today())
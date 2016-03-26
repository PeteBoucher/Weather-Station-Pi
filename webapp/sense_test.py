from sense import Sense

sensors = Sense()

log = sensors.read_log()
# print log

conditions = sensors.current_conditions()
print 'Last sensor log entry:', conditions[0]

print 'Temperature in deg C:', conditions[1]
print 'Pressure in mBar:', conditions[2]
print 'Relative Humidity:', conditions[3]
print 'Last reading was taken at:', conditions[4]
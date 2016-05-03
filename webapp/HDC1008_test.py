from HDC1008 import HDC1008

sensor = HDC1008(0x40)

print 'Temperature:', sensor.get_temp()
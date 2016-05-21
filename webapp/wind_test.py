from wind import Wind

wind_sensors = Wind()

print 'Wind anemometer rpm:', wind_sensors.speed(23,10000000)
print 'Wind speed in km/h:', wind_sensors.get_speed('km/h')
print 'Wind direction in degrees:', wind_sensors.get_direction()

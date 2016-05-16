from wind import Wind

wind_sensors = Wind()

print 'Wind speed in km/h:', wind_sensors.get_speed('km/h')
print 'Wind direction in degrees', wind_sensors.get_direction()
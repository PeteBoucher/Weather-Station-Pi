Rasperry Pi Weather Station
===========================

This is a project the kids wanted to do after learing about climate and 
weather at school.

We're using a Raspery Pi 2 model B as the controller and some air sensors
from Adafruit. The controller is housed in a PVC exterior housing from
the hardwarestore and we fabricated a Stephenson housing for the sensors
out of up-cycled plastic bottles.

We also intend to add wind speed and direction sensors and a rain guage at
a later date.

Sersor package:
---------------
MPL3115A2 Atmospheric pressure and temperature sensor from Adafruit
HDC1008	  Temperature and relative humidity sensor from Adafruit

Instalation
-----------

The weather station runs on the standard Raspbian OS.

copy the startup script I2C_combined to /etc/init.d/ and register it to be 
run at startup this is required for the MPL3115A2 sensor to respond properly
to requests as it requires someting called a repeated start or combined mode
from the I2C deriver to operate. I also made root the owner of this script 
but I'm not sure that is required.
```
$ sudo cp I2C_combined /etc/init.d
$ sudo chmod 755 /etc/init.d/I2C_combined
$ sudo chown root /etc/init.d/I2C_combined
$ sudo update-rc.d I2C_combined defaults
```
Add a cron job to the crontab of root (all python scripts that interact with
hardware components must be run as root)
```
sudo crontab -e
```
Add a line that will launch the script that performs all the sensor readings
and writes the results to storage. I have my weather station doing this every 
10 minutes. You can also supress the normal email reports with `>/dev/null 2>&1`
if you have mail installed on the Raspberry Pi.
```
*/10 * * * * python /home/pi/weather/take_redaings.py >/dev/null 2>&1
```

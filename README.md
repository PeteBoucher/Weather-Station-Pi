Raspberry Pi Weather Station
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
- MPL3115A2 Atmospheric pressure and temperature sensor from Adafruit
- HDC1008	  Temperature and relative humidity sensor from Adafruit

Instalation
-----------

The weather station runs on the standard Raspbian OS.

You'll need to install I2C packages for the python code to access sensor
hardware connected to the I2C bus.
```
sudo apt-get install i2c-tools python-smbus
```
Copy the startup script I2C_combined to /etc/init.d/ and register it to be 
run at startup this is required for the MPL3115A2 sensor to respond properly
to requests as it requires someting called a repeated start or combined mode
from the I2C deriver to operate. I also made root the owner of this script 
but I'm not sure that is required.
```
sudo cp I2C_combined /etc/init.d
sudo chmod 755 /etc/init.d/I2C_combined
sudo chown root /etc/init.d/I2C_combined
sudo update-rc.d I2C_combined defaults
```
Add a cron job to the crontab of root (all python scripts that interact with
hardware components must be run as root)
```
sudo crontab -e
```
Add a line that will launch the script that performs all the sensor readings
and writes the results to storage. I have my weather station doing this every 
10 minutes. Replace `/home/pi` with the absolute path tou your fork of the repo. 
You can also supress the normal email reports with `>/dev/null 2>&1`if you have 
mail installed on the Raspberry Pi.
```
*/10 * * * * python /home/pi/Weather_Station_Pi/take_redaings.py >/dev/null 2>&1
```
Hardware
________
For wiring you just need to connect the power and ground of your sensors to pins
1 (3.3V) and 2 (GND). And connect the I2C data and clock pins to 3 (SDA) and
5 (SCL). Multiple sensors can be connected in series (daisy chain). Check the
pinout and voltage requirements on your sensors if they differ from my HW.

Web UI
------
Theres a simple flask web interface. To use it install the Python package manager
and flask web framework:
```
sudo apt-get update
sudo apt-get install -y python-pip python-dev
sudo pip install flask
```
Thanks to Tony D https://github.com/tdicola for the how to video on creating a 
Flask Internet Thing https://github.com/adafruit/Pi_Internet_Thing_Videos

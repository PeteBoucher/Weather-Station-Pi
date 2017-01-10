# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # Print the ADC values.
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.5)

## RESULTS
#| dir  | ch0  | ch1  | ch2  | ch3  | ch4  | ch5  | ch6  | ch7  |
#|  000 |  928 |  539 |  384 |  334 |   10 |    0 |    0 |    0 |
#|  000 |  928 |    0 |   13 |   16 |   15 |   18 |   18 |  371 |
#|  045 |  837 |  589 |  504 |  475 |  341 |  310 |  288 |  197 |
#|  045 |  836 |  242 |    0 |    0 |    0 |    0 |    0 |    0 |
#|  090 |  732 |    1 |   21 |   17 |  418 |  527 |  517 |  500 |
#|  090 |  731 |  557 |  409 |  350 |  239 |  201 |  203 |    0 |
#|  135 |  387 |    0 |    0 |    0 |    5 |   12 |   21 |   15 |
#|  135 |  392 |  358 |  528 |  512 |  500 |  494 |  460 |  309 |
#|  180 |   77 |  535 |  377 |  251 |    0 |    0 |    0 |    0 |
#|  180 |   76 |    0 |   16 |   18 |   14 |   16 |  119 |  517 |
#|  225 |  139 |  584 |  489 |  442 |  298 |  260 |  245 |  170 |
#|  270 |  231 |  117 |    0 |    0 |    0 |    0 |    0 |   11 |
#|  270 |  234 |    2 |   22 |  346 |  517 |  528 |  506 |  490 |
#|  315 |  558 |  551 |  400 |  346 |  236 |  200 |    0 |    0 |
#|  000 |  929 |    0 |    0 |    0 |   13 |   21 |   22 |   14 |
#|  000 |  928 |  489 |  530 |  504 |  478 |  490 |  388 |  261 |


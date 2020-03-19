#!/usr/bin/env python

import math
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D8)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P0)

# steinhart
B = 3435
value = channel.value
resistance = (65536-value)*(10000/value)
temp = (1/(math.log(resistance/10000)/B+1/298.15)-273.15)
print(format(temp*(9/5.0)+32, '.0f') + 'F')

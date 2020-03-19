# Air Control
This collection of software is used on a Raspberry PI with a MCP3008 ADC and some relay's.
The intent is to create a modular system that:
1. Easily add Raspberry PI's to the network, and
2. Have a simple web interface for any web device to have control

### Requirements
These programs have some requirements before running:
1. [RPi.GPIO]("https://pypi.org/project/RPi.GPIO/")
2. [Adafruit Circuitpython MCP3008 library]("https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx") `sudo pip3 install adafruit-circuitpython-mcp3xxx`
3. Working [Apache web server]("https://httpd.apache.org/")
  - also requires mod_python to be installed
    - `apt install libapache2-mod-python` (for debian systems)
      - (also requires configuration, which notes are here)
4. ac_unit_server.py uses ssh to send commands to computers listed in COMPUTERS, so an SSH server on these computers will need to be installed. These computer will _need_ no password authentication set up to work properly.
5. **Have relays, MCP3008 wired properly!** (add content later)
6. (Optional) This is currently being used as a simple automation system for a workshop, and as so there is no networking. For this case, the (Master) Raspberry PI is setup with a WiFi antenna and configured as an access point, with the capability of other (Slave) wireless devices connecting to its network.

### File System Hierarchy
- html folder will be installed in `/var/www/`.
- \*.py files should be installed in the user root directory for simplicity.

### How to use
Once a Raspberry PI is setup, point a web browser on the same network to the devices web page, and the page should be intuitive!
The Python programs drive relay's that control devices. </br>
In a current case:
- `actuator-control.py` controls a relay connected to an actuator controlling the opening and closing of a window.
- `compressor-contro.py` controls a relay connected to a compressor on a AC unit and ensures safe operation of the compressor.
- `fan-control.py` controls a relay connected to a fan on the respective AC unit as the compressor.
- `get_temp.py` receives an analog value from MCP3008 and uses Steinhart-Hart equation to get a temperature reading from a [NTC 10k Thermistor Temperature Probe]("https://www.adafruit.com/product/372") setup in a voltage divider.

### Annoyances
The web server waits for python programs to complete causing a few seconds of lag on the web server.

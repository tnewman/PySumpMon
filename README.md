# PySumpMon
PySumpMon is a Sump Pump Monitor using Python and Arduino. The Arduino uses the 
[EVShield](http://www.mindsensors.com/arduino/12-evshield-with-arduino-uno-compatible-board-bundle) 
to determine the distance to the water in sump. As distances are read by the Arduino every second, 
they are sent to a Python server over serial. The Python server polls the serial port every 
30 seconds. The current distance is then logged and can be viewed on a web page. If the distance 
to the water is less than 10 cm, a text message is sent via Twillio using the parameters set in the 
configuration file.

# License
[MIT License](https://github.com/tnewman/PySumpMon/blob/master/LICENSE)

# Prerequisites
1. Computer to run the Python server
2. [Arduino with EVShield](http://www.mindsensors.com/arduino/12-evshield-with-arduino-uno-compatible-board-bundle)
3. [NXT Ultrasonic Sensor](http://shop.lego.com/en-US/Ultrasonic-Sensor-9846)
4. [Arduino IDE](https://www.arduino.cc/en/Main/Software)
5. [Python 3](https://www.python.org/downloads)
6. [GIT](https://git-scm.com)
7. [Twilio Trial Account](https://www.twilio.com)

# Installation and Usage
These installation instructions are for Windows and will need to be modified for Linux.

## Obtaining PySumpMon
1. Open the command prompt
2. Navigate to the root directory using the command `cd C:/`
3. Clone this Git repository using `git clone https://github.com/tnewman/PySumpMon`

## Arduino
1. Connect the EVShield to the Arduino
2. Connect the NXT Ultrasonic Sensor to port `BAS1` on the EVShield
3. Connect the USB cable to the Arduino and the PC
4. Install the `PySumpMon/ArduinoDistance/ArduinoDistance.ino` sketch on the Arduino 
   using the Arduino Software

## Python Server
1. Open the command prompt
2. Navigate to the `PySumpMonFolder` using the command `cd C:/PySumpMon`
3. Initialize the database using the command `python dbinit.py`
4. Open the file `pysumpmon/config.py` in a text editor
5. Set `DISTANCE_SENSOR_PORT` to the serial port for the Arduino
6. Set `TWILLIO_ACCOUNT` to the account credential provided by Twilio
7. Set `TWILLIO_TOKEN` to the token credential provided by Twilio
8. Set `TWILLIO_NOTIFICATION_FROM` to the phone number that will be used to send the 
   message provided by Twilio
9. Set `TWILLIO_NOTIFICATION_TO` to the phone number that the text messages should 
   be sent to.

## Running
1. Point the NXT Ultrasonic Sensor at the bottom of the sump pump
2. Connect the Arduino to the PC
3. Open the command prompt
4. Navigate to the `PySumpMonFolder` using the command `cd C:/PySumpMon`
5. Run the Python Server with the command `python app.py`
6. Distance can be viewed by going to the page [http://localhost:5000](http://localhost:5000) 
   in your web browser.

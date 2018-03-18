This project was built to detect potholes, record GPS coordinates, date & time and display the results on a google map.

Features

1) yellow LED 
	This LED provides visible status on whether or not the runme.py program is running.    If the python program is running, then the LED is on

2) red LED
	This LED provides visible status on whether or not the WIFI has internet access to the amazon cloud server.   If no internet, the LED is ON.    

3) green LED
	This LED provides visible status on whether or not data uploads are in progress.   If the uploading is occurring, the LED is ON.

4) blue LED
	This LED provides visible status on whether or not GPS fix has occurred.    If the LED is flashing,  the GPS unit is busy acquiring Satellites

5) white LED
	This LED provides visible status on whether or not a vibration was detected.    If the LED is ON,  a vibration was sensed and recorded

7) vibration sensor
	This hardware component will detect vibrations.   The operation of this component compares to a switch.    The component is considered open until a vibration occurs at 
	which point the component closes

7) button to force cloud update
	This button runs forces data transfers to the cloud.    When pressed, this button executes code that turns on the green LED and uploads the gps.dat file to the cloud

8) gps logging
	This component communicates with GPS satellites to acquire Latitude, Longitude coordinates.     This device communicates with the PI over the serial port

9) application features
	
	This app will continue to run and record GPS locations if there is no access to the internet.   Once the internet is available, the app will upload data every 5 mins or
	a person can force an update with the button


-----------------------------------------------------------------------------------------------------------------------

gps-v4.0.3 – latest code

runme.py -  this is a copy of the latest working code.   runme.py must to be stored in /home/pi/Documents folder

gps.dat – sample gps data

Wiring.png –wiring diagram 

-----------------------------------------------------------------------------------------------------------------------






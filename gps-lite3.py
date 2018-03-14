import serial
from time import sleep
import os
import RPi.GPIO as GPIO

ser=serial.Serial('/dev/ttyAMA0',9600)

filename = '/home/pi/Documents/gps.dat'
if os.path.exists(filename):
        os.remove(filename)

GPSdata=open(filename, 'w')
GPSdata.close()

class GPS:
        def __init__(self):
                GPRMC_GPGGA="$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n"#Send GPRMC AND GPGGA Sentences
                UPDATE_1_sec=  "$PMTK220,1000*1F\r\n"   #Update Every One Second
                MEAS_1_sec = "$PMTK300,1000,0,0,0,0*1C\r\n"   #Measure once a second
                BAUD_57600 = "$PMTK251,57600*2C\r\n"          #Set Baud Rate at 57600
                BAUD_9600 ="$PMTK251,9600*17\r\n"             #Set 9600 Baud Rate
                
                # Setting up the rate in which the GPS communicates and passes data to our program
                ser.flushInput()
                ser.flushInput()  
                ser.write(BAUD_57600) 
                sleep(1)   # sleep commands allow the GPS to process what we sent to it
                ser.baudrate=57600
                sleep(1)
                ser.write(UPDATE_1_sec)
                sleep(1)
                ser.write(MEAS_1_sec)
                sleep(1)
                ser.write(GPRMC_GPGGA)
                sleep(1)
                ser.flushInput()  # flushing the toliet and ridding ourselfs of any serial buffer data prior to parsing good GPS sentences
                ser.flushInput()
                os.system('clear')
                
                print ("----------------------------------")
                print ("- GPS Configuration Initialized! -")
                print ("----------------------------------")
                print ("- Update Speed  : 1 Sec          -")
                print ("- Measure speed : 1 Sec          -")
                print ("- BaudRate      : 56k            -")
                print ("----------------------------------\n")
                print ("Awaiting Potholes...\n")
                
        def read(self):

                # Poor Man's way of clearing the serial buffer and then waiting for serial data
                ser.flushInput()
                ser.flushInput()
                
                while ser.inWaiting()==0:
                        pass
                self.NMEA1=ser.readline()
            
                while ser.inWaiting()==0:
                        pass
                self.NMEA2=ser.readline()

                # Parse NMEA data into meaniful variables                
                NMEA1_array=self.NMEA1.split(',')
                NMEA2_array=self.NMEA2.split(',')
                if NMEA1_array[0]=='$GPRMC':
                        self.timeUTC=NMEA1_array[1][:-8]+':'+NMEA1_array[1][-8:-6]+':'+NMEA1_array[1][-6:-4]                                                                                           
                        self.latDeg=NMEA1_array[3][:-7]
                        self.latMin=NMEA1_array[3][-7:]
                        self.latHem=NMEA1_array[4]
                        self.lonDeg=NMEA1_array[5][:-7]
                        self.lonMin=NMEA1_array[5][-7:]
                        self.lonHem=NMEA1_array[6]
                        self.knots=NMEA1_array[7]
                        self.date=NMEA1_array[9][-4:-2]+'-'+NMEA1_array[9][:-4]+'-20'+NMEA1_array[9][-2:]
                        
                if NMEA1_array[0]=='$GPGGA':
                        self.fix=NMEA1_array[6]
                        self.altitude=NMEA1_array[9]
                        self.sats=NMEA1_array[7]
                if NMEA2_array[0]=='$GPRMC':
                        self.timeUTC=NMEA2_array[1][:-8]+':'+NMEA1_array[1][-8:-6]+':'+NMEA1_array[1][-6:-4]
                        self.latDeg=NMEA2_array[3][:-7]
                        self.latMin=NMEA2_array[3][-7:]
                        self.latHem=NMEA2_array[4]
                        self.lonDeg=NMEA2_array[5][:-7]
                        self.lonMin=NMEA2_array[5][-7:]
                        self.lonHem=NMEA2_array[6]
                        self.knots=NMEA2_array[7]
                        self.date=NMEA2_array[9][-4:-2]+'-'+NMEA2_array[9][:-4]+'-20'+NMEA2_array[9][-2:]  
                if NMEA2_array[0]=='$GPGGA':
                        self.fix=NMEA2_array[6]
                        self.altitude=NMEA2_array[9]
                        self.sats=NMEA2_array[7]

myGPS=GPS()


Sensor1=21  #GPIO 21 pin for Sensor1 detection

GPIO.setmode(GPIO.BCM)
GPIO.setup(Sensor1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

def bump(channel):

        myGPS.read()
        os.system('clear')
        print ("Sensor1 Detected a stinking pothole!")
        print ("UTC: " + myGPS.timeUTC)
        print ("DATE:" + myGPS.date)
        
        if myGPS.fix!=0:
                latDec=float(myGPS.latDeg)+float(myGPS.latMin)/60.
                lonDec=float(myGPS.lonDeg)+float(myGPS.lonMin)/60.
                
                if myGPS.lonHem=='W':
                        lonDec=(-1)*lonDec
                if myGPS.latHem=='S':
                        latDec=(-1)*latDec
                
                alt=myGPS.altitude
                
                GPSdata=open(filename, 'a')
                myString=str(lonDec)+','+str(latDec)+','+alt+' '
                GPSdata.write(myString+ "\n")
                GPSdata.close()
                print ("GPS: " + myString + "\n")              

GPIO.add_event_detect(Sensor1,GPIO.RISING,callback=bump, bouncetime=600)

try:
        while True:
                sleep(120)  # this is very important sleep; otherwise the PI consumes CPU
                pass
                
except (KeyboardInterrupt, SystemExit):
        print "\nExisting...."

print ("GPS De-Configured & GPIO pins cleaned up!")

ser.flushInput()
ser.flushInput()  
ser.write("$PMTK251,9600*17\r\n") 
sleep(1)   # sleep commands allow the GPS to process what we sent to it
GPIO.cleanup()
print ("Bye bye!")            
            

import serial
from time import sleep
import RPi.GPIO as GPIO

ser=serial.Serial('/dev/ttyAMA0',9600)

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
                ser.write(UPDATE_1_sec)
                sleep(1)
                ser.write(MEAS_1_sec)
                sleep(1)
                ser.write(GPRMC_GPGGA)
                sleep(1)
                ser.flushInput()  # flushing the toliet and ridding ourselfs of any serial buffer data prior to parsing good GPS sentences
                ser.flushInput()
                print ("GPS Initialized")
        def read(self):
                #ser.flushInput()
                #ser.flushInput()

                while ser.inWaiting()==0:
                        pass
                
                self.NMEA1=ser.readline()
            
                
                while ser.inWaiting()==0:
                        pass
                
                self.NMEA2=ser.readline()
                
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
 
                if NMEA2_array[0]=='$GPGGA':
                        self.fix=NMEA2_array[6]
                        self.altitude=NMEA2_array[9]
                        self.sats=NMEA2_array[7]

myGPS=GPS()
GPSdata=open('/home/pi/Documents/GPS.txt', 'w')
GPSdata.close()

POTHOLE=21  #GPIO 21 pin for pothole detection

GPIO.setmode(GPIO.BCM)
GPIO.setup(POTHOLE,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

def bump(channel):
        print ("pothole detected")
        myGPS.read()
        
        if myGPS.fix!=0:
                latDec=float(myGPS.latDeg)+float(myGPS.latMin)/60.
                lonDec=float(myGPS.lonDeg)+float(myGPS.lonMin)/60.
                
                if myGPS.lonHem=='W':
                    lonDec=(-1)*lonDec
                if myGPS.latHem=='S':
                    latDec=(-1)*latDec
                
                alt=myGPS.altitude
                
                GPSdata=open('/home/pi/Documents/GPS.txt', 'a')
                myString=str(lonDec)+','+str(latDec)+','+alt+' '
                print(myString + "\n")
                GPSdata.close()
                

GPIO.add_event_detect(POTHOLE,GPIO.RISING,callback=bump, bouncetime=600)

try:
        while True:
                sleep(120)  # this is very important sleep; otherwise the PI consumes CPU
                pass

except (KeyboardInterrupt, SystemExit):
        print "\nExisting...."

ser.flushInput()
ser.flushInput()  
ser.write("$PMTK251,9600*17\r\n") 
sleep(1)   # sleep commands allow the GPS to process what we sent to it
                
            

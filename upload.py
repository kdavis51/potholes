import ftplib

s = ftplib.FTP('ec2-34-234-70-61.compute-1.amazonaws.com','myftpuser','myftpuser')

f = open('/home/pi/Documents/gps.dat','rb')
s.storbinary('STOR gps.dat' ,f)
f.close()
s.quit()
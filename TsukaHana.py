import time
import numpy as np
import wiringpi as pi
import socket
import sys

SPI_CH = 0
READ_CH = 0
direction = 0
pi.wiringPiSPISetup(SPI_CH, 1000000 )

motor11_pin = 23
motor12_pin = 24
motor21_pin = 22
motor22_pin = 27
pi.wiringPiSetupGpio()
pi.pinMode( motor11_pin, 1 )
pi.pinMode( motor12_pin, 1 )
pi.pinMode( motor21_pin, 1 )
pi.pinMode( motor22_pin, 1 )
pi.softPwmCreate( motor11_pin, 0, 1024)
pi.softPwmCreate( motor12_pin, 0, 1024)
pi.softPwmCreate( motor21_pin, 0, 1024)
pi.softPwmCreate( motor22_pin, 0, 1024)
pi.softPwmWrite( motor11_pin, 0 )
pi.softPwmWrite( motor12_pin, 0 )
pi.softPwmWrite( motor21_pin, 0 )
pi.softPwmWrite( motor22_pin, 0 )

while True:
    try:
        buffer = 0x6800 |  (0x1800 * READ_CH ) 
        buffer = buffer.to_bytes( 2, byteorder='big' )
        
        pi.wiringPiSPIDataRW( SPI_CH, buffer )
        value = 1024 - ( buffer[0] * 256 + buffer[1] ) & 0x3ff
        print ("value :" , value)
        if (value < 350):
            vi = (400 - value) *2
            pi.softPwmWrite( motor11_pin, vi )
            pi.softPwmWrite( motor12_pin, 0 )
            pi.softPwmWrite( motor21_pin, vi )
            pi.softPwmWrite( motor22_pin, 0 )
        if (value > 500):
            vi = (value - 450) * 2
            pi.softPwmWrite( motor11_pin, 0 )
            pi.softPwmWrite( motor12_pin, vi )
            pi.softPwmWrite( motor21_pin, 0 )
            pi.softPwmWrite( motor22_pin, vi )


    except KeyboardInterrupt:
        break

pi.softPwmWrite( motor11_pin, 0 )
pi.softPwmWrite( motor12_pin, 0 )
pi.softPwmWrite( motor21_pin, 0 )
pi.softPwmWrite( motor22_pin, 0 )

print('Stop Streaming')

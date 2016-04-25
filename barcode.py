import time
import serial
import os
import sys
import binascii
#from bbio import *
from ledstatus import *
def readID():
    rcv = 'blank'
    timecnt = 5
    while timecnt:
        timecnt = timecnt-1
        if "/dev/ttyACM0" in os.popen("ls /dev/ttyACM*").read() and "/dev/ttyACM1" in os.popen("ls /dev/ttyACM*").read():
            break
        time.sleep(1)
    
    try:
        port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=0.5)
    except:
        try:
            port = serial.Serial("/dev/ttyACM1", baudrate=115200, timeout=0.5)
        except IOError:
            print "cannt read /dev/ttyACM1 or /dev/ttyACM0"
            ledindex = ledstatus(7)
            return rcv
    ledindex = ledstatus(0)
    print port
    while True:
        rcv = port.read(12)
        print rcv
        port.flush()
        if(rcv != '' and rcv[0:3] == 'BBG' and rcv[-1] >= '0' and rcv[-1] <= '9'):
            break
    ledindex.led_clear = 1
    return rcv
if __name__ == '__main__':
    print readID()    


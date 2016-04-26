#/usr/bin/env python
import sys
import os
import binascii
import string
import time
import barcode
import  serial
import platform
import Ethenet_sing
import pins
from  ledstatus  import *
from fileModule import *
from  operate_eeprom import *
import mraa
import barcode_kbd
import multiprocessing

OK_PIN = 88  # "P9_42"
NG_PIN = 87  # "P9_41"
TEST_PIN = 77  # "P9_31"

ng_pin = mraa.Gpio(NG_PIN)
ok_pin = mraa.Gpio(OK_PIN)
test_pin = mraa.Gpio(TEST_PIN)

ng_pin.dir(mraa.DIR_OUT)
ok_pin.dir(mraa.DIR_OUT)
test_pin.dir(mraa.DIR_OUT)

ng_pin.write(0)
ok_pin.write(0)
test_pin.write(0)

def lock():
        print "lock!"
        while True:
            pass

'''
def checkDebugUart():
    uart = serial.Serial(port = "/dev/ttyUSB0", baudrate=9600)
    uart.flush()
'''
        

def runError(pid):
    _pid = str(pid)
    os.system("kill -9 " + _pid)
    t_error = ledstatus(7)
    t_error.led_clear = 1
    cnt = 0
    os.system("sync")
    os.system("sync")
    os.system("sync")
    while True:    
        ng_pin.write(0)        # GPIO.output(NG_PIN,GPIO.LOW)
        time.sleep(0.5)
        ng_pin.write(1)        # GPIO.output(NG_PIN,GPIO.HIGH)
        time.sleep(0.5)

def report_error():    
    pid = os.getpid()
    p = multiprocessing.Process(target = runError, args = (pid,))
    p.start()

if __name__ == '__main__': 
    try:
        test_pin.write(1)    #GPIO.output(TEST_PIN,GPIO.HIGH)    
        ng_pin.write(1)        # GPIO.output(NG_PIN,GPIO.HIGH)
        time.sleep(0.5)
        ok_pin.write(0)        # GPIO.output(OK_PIN,GPIO.LOW)
        ng_pin.write(0)        # GPIO.output(NG_PIN,GPIO.LOW)    

        #id = 'BBG115051111'   
        print  "start readID"
        id = barcode_kbd.readID().encode("utf-8")        
        report_file = id
        okfile = id
        #report_file = 'BBG115051111'
        print  report_file
        
        #report = open(report_file,'w+')
        #report.write("-------------- Barcoder test ----------- \n")
        if report_file != 'blank':
            usbfile = open("/proc/mounts",'r')
            while True:
                line = usbfile.readline()
                a = line.find("media")
                if a != -1 :
                    report_file = line.split()[1]+"/report/"+report_file+'_fail'+".txt"
                    okfile = line.split()[1]+"/report/"+okfile+'_pass'+".txt"
                    break
                    
            report = open(report_file,'w+')
        else:        
            report_error()
        report.write("That's BealgeBone Green  Seiral:" + report_file + " production test report!\n")
        report.write("if you have any questions about this test reports,Please conntact:www.seeedstudio.com\n")
        report.write("Software System:" + platform.linux_distribution()[0] + ' ' + platform.linux_distribution()[1] + '\n')
        report.write("Software Version:\n")

        versionfile = FM('version')
        report.write(versionfile.readFileText())

        report.write("Hardware test:\n")
        report.write("************************************************************************\n")

        '''eeprom test'''
        report.write("-------------------------------eeprom test------------------------------\n")
        Myeeprom = eeprom()
        name,version,serial = Myeeprom.readBoardinfo()

        version = 'BBG1'
        serial = id
        print type(serial)
        Myeeprom.writeBoardinfo(name,version,serial)
        name,version,serial = Myeeprom.readBoardinfo()
        if serial == id:
            report.write('write board serial: ' + serial + '------>[pass]\n\n')
            report.write('write board version: ' + '%s'%version + '------>[pass]\n\n')
        else:
            report.write('write board serial: ' + serial + '------>[fail]\n\n')
            report.write('write board version: ' + '%s'%version + '------>[fail]\n\n')
            report.close()
            report_error()
            
        '''DDR test'''
        report.write("--------------------------------DDR test------------------------------\n")
        ddr_file = FM('DDR')
        ddrsize = float(ddr_file.readMemory()[0:6])
        print  'ddrsize: ', ddrsize
        # if ddrsize > 507904:
        if ddrsize > 503904:
            report.write('DDR size: ' + ddr_file.readMemory() + '------>[pass]\n\n')
        else:
            report.write('DDR size: ' + ddr_file.readMemory() + '------>[fail]\n\n')
            report.close()
            report_error()
        
        '''eMMC test'''
        report.write("-------------------------------eMMC test------------------------------\n")
        emmcsize = ddr_file.getemmcsize()
        if emmcsize > 3.6:
            report.write('eMMc size: ' + '%f'%emmcsize + ' GB ------>[pass]\n\n')
        else:
            report.write('eMMc size: ' + '%f'%emmcsize + ' GB ------>[fail]\n\n')
            report.close()
            report_error()    
        
        '''Debug Uart test'''
        print "Debug Uart test"
        report.write("----------------------------Debug Uart test---------------------------\n")

        if pins.check_debug_uart() == 'ok':
            report.write("Debug Uart test   ------>[pass]\n\n")
        else:
            report.write("Debug Uart test   ------>[fail]\n\n")
            report.close()
            report_error()    
            
        # Grove Uart test
        print "Grove Uart test"
        report.write("----------------------------Grove Uart test---------------------------\n")
        os.system("echo BB-UART2 > /sys/devices/platform/bone_capemgr/slots")
        os.system("sync")
        os.system("sync")
        os.system("sync")
        if pins.check_uart() == 'ok':
            report.write("Grove Uart test   ------>[pass]\n\n")
        else:
            report.write("Grove Uart test   ------>[fail]\n\n")
            report.close()
            report_error()
        
        # Grove I2C test
        print "Grove I2C test"
        report.write("----------------------------Grove I2C test----------------------------\n")
        if pins.check_i2c() == 'ok':
            report.write("Grove I2C test   ------>[pass]\n\n")
        else:
            report.write("Grove I2C test   ------>[fail]\n\n")
            report.close()
            report_error()
            
        
        # analog pins test
        print "analog pins test"
        report.write("----------------------------analog pins test---------------------------\n")
        status,result = pins.check_voltage()
        for v in result:
            report.write(v+'\n')
        if status == 'ok':
            report.write("analog pins test   ------>[pass]\n\n")
        else:
            report.write("analog pins test   ------>[fail]\n\n")
            report.close()
            report_error()
        
        
        # PMU test
        print "PMU test"
        report.write("----------------------------PMU test---------------------------\n")
        status,result = pins.check_power()
        for v in result:
            report.write(v+'\n')
        if status == 'ok':
            report.write("PMU test   ------>[pass]\n\n")
        else:
            report.write("PMU test   ------>[fail]\n\n")
            report.close()
            report_error()
        
        
        # GPIO test
        print "GPIO test"
        report.write("------------------------------ GPIO test------------------------------\n")
        badio = []
        # os.system("config-test-gpio overlay gpio-test")
        badio = pins.check_io()
        if len(badio) != 0:
            report.write("gpio test ------>[fail]\n\n")
            for pin in badio:
                report.write(str(pin) +'\n')
            report.close()
            report_error()
        else:
            report.write("gpio test ------>[pass]\n\n")
        
        
        # Net test
        print "Net test"
        report.write("-------------------------------Net test-------------------------------\n")
        if Ethenet_sing.do_ethernet_dhcp() != 'ok':
            report.write("Ethernet test ------->[fail]\n\n")
            report.close()
            report_error()
        else:
            report.write("Ethernet test ------->[passed]\n\n")
        report.write("Board ethernet mac address :"+Ethenet_sing.get_mac_addr()['eth0']+'\n')    
        
        
        # OTG test
        print "OTG test"
        report.write("-------------------------------OTG test-------------------------------\n")
        if ddr_file.check_otg_disk() == 'ok':
            report.write("OTG test   ------>[pass]\n\n")
        else:
            report.write("OTG test   ------>[fail]\n\n")
            report.close()
            report_error()
        report.write("************************************************************************\n")
        P8_43 = mraa.Gpio(43)    #GPIO.setup('P8_43', GPIO.IN)
        P8_43.dir(mraa.DIR_IN)
        ok_pin.dir(mraa.DIR_OUT)   #GPIO.setup(OK_PIN,GPIO.OUT)
        test_pin.dir(mraa.DIR_OUT)   #GPIO.setup(TEST_PIN,GPIO.OUT)

        ok_pin.write(1)    #GPIO.output(OK_PIN,GPIO.HIGH)
        test_pin.write(0)   #GPIO.output(TEST_PIN,GPIO.LOW)
        while True:
            if P8_43.read() == 0:
                report.write("sd button test ok!")
                break

        report.close()
        '''    
        # Remove factory files
        os.system("rm /etc/need_test")
        os.system("rm /opt/scripts/boot/factory_check.sh")                  
        os.system("rm /lib/systemd/system/factory-check.service")
        
        # uEnv.txt             
        os.system("sed -e 's/dtb=am335x-bonegreen.dtb/#dtb=/' /boot/uEnv.txt > /root/uEnv.txt")
        os.system("sed 's/cmdline=coherent_pool=1M quiet cape_universal=disable/cmdline=coherent_pool=1M quiet cape_universal=enable/' /root/uEnv.txt > /root/temp")
        os.system("cat /root/temp > /root/uEnv.txt")
        os.system("mv /root/uEnv.txt /boot/uEnv.txt")
        os.system("rm /root/temp")
        # am335x_evm.sh
        os.system("sed '163,166d' /opt/scripts/boot/am335x_evm.sh > /root/am335x_evm.sh")
        os.system("sed '80d' /root/am335x_evm.sh > /root/temp")
        os.system("mv /root/temp /opt/scripts/boot/am335x_evm.sh")
        os.system("rm /root/am335x_evm.sh")
        '''
        os.system("sync")
        os.system("sync")
        os.system("sync")
        os.system("mv "+report_file+" "+okfile)
        os.system("sync")
        os.system("sync")
        os.system("sync")

        ok_pin.write(0)    #GPIO.output(OK_PIN,GPIO.LOW)
    except Exception as e:        
        report.write("\r\n------------------------------- Other error -------------------------------\n")        
        error = ''
        for e in e.args:
            error += str(e)
        report.write(error)
        report.write("\r\n")
        report.close()
        sys.exit()
        #report_error()
    except (KeyboardInterrupt, SystemExit):
        report.close()
        #report_error()        
        sys.exit()


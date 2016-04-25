import os
import threading

print os.getcwd()
os.chdir("/media/usb1/python-evdev/")
os.system("python setup.py install")
os.chdir("/media/usb1")

def run():
    os.system("python BBG_produce_2.py")
    
t = threading.Thread(target=run)
t.start()
print "exit"
exit(0)
import os
import multiprocessing

print os.getcwd()
os.chdir("/media/usb1/python-evdev/")
#os.system("python setup.py install")
os.chdir("/media/usb1")

def run():    
    os.system("python BBG_produce_2.py")
    
p = multiprocessing.Process(target=run)
p.start()
print "exit"
exit(0)
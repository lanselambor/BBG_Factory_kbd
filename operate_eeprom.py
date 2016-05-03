import os
import sys
import struct
'''
struct am335x_baseboard_id {
       u8 magic[4];
       u8 name[8];
       u8 version[4];
       u8 serial[12];
       u8 config[32];
       u8 mac_addr[3][6];
};
#define as I8sI12s32s18s
'''
class eeprom:
    def __init__(self,dumpName = ''):
        self.eeprom_dump = struct.Struct("I8s4s12s32s18s")



    def readBoardinfo(self):
        self.fp_sys = open('/sys/devices/platform/ocp/44e0b000.i2c/i2c-0/0-0050/at24-0/nvmem','rb')
        self.eeprom_dump = self.fp_sys.read(78)

        self.magic,\
        self.name,\
        self.version,\
        self.serial,\
        self.config,\
        self.mac_addr = \
            struct.unpack("I8s4s12s32s18s",self.eeprom_dump)

        self.fp_sys.close()
        return self.name,self.version,self.serial


    def writeBoardinfo(self,new_name,new_version,new_serial):
        self.fp_local = open('eeprom.dump','wb+')
        self.name = new_name
        self.version = new_version
        self.serial = new_serial
        #print 'info .......'
        #print self.name
        #print self.version
        #print self.serial
        self.eeprom_dump = struct.pack('I8s4s12s32s18s', self.magic,\
                                                        self.name,\
                                                        self.version,\
                                                        self.serial,\
                                                        self.config,\
                                                        self.mac_addr)
        self.fp_local.write(self.eeprom_dump)
        self.fp_local.close()

    	os.system("dd if=./eeprom.dump of=/sys/devices/platform/ocp/44e0b000.i2c/i2c-0/0-0050/at24-0/nvmem")
        os.system("sync")


#Test eeprom class
if __name__ == '__main__':
	Myeeprom = eeprom()
        # read
	name,version,serial = Myeeprom.readBoardinfo()
	print name
	print version
	print serial
        # write
	version = 'BBG1'
	serial = 'BBG215050012'
	Myeeprom.writeBoardinfo(name,version,serial)

	name,version,serial = Myeeprom.readBoardinfo()
	print name
	print version
	print serial

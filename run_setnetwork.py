import os 
import smbus 
import time
import json
#grep -r ifconfig *

Default_IP = "192.168.125.35"
def check_byte(l):
    total_sum = 0
    for c in range(0,len(l)):
        total_sum = total_sum + l[c]
    value_LI  = total_sum & 0xff
    value_HI  = (total_sum >> 8) & 0xff
    return value_LI,value_HI 
        



bus =smbus.SMBus(1)

for j in range(0,10):
    dat = bus.read_i2c_block_data(0x30,11,12)
    value_LI,value_HI = check_byte(dat[0:10])
    
    if (dat[0] == 0xff and dat[1] == 0xff and dat[2] ==0xff and dat[3] == 0xff) or (dat[0] == 0 and dat[1] == 0 and dat[2] ==0 and dat[3] == 0):
        _IP_BUFFER = Default_IP
        
        #_IP_BUFFER = '.'.join([str(i) for i in _IP_BUFFER[0:4]]) 
    else:
        _IP_BUFFER = '.'.join([str(i) for i in dat[0:4]])     
    if dat[10] != value_LI or dat[11] != value_HI:
        _IP_BUFFER = Default_IP
        print "ip read error "
        time.sleep(0.2)
    else:
        print "ip read right " 
        print _IP_BUFFER 
        break


print "_IP_BUFFER",_IP_BUFFER
fh = open('/home/pi/hf_formation/hf.conf','r')
contents = fh.read()
print contents
fh.close()
obj_json = json.loads(contents)
obj_json['ip'] = _IP_BUFFER
fh = open('/home/pi/hf_formation/hf.conf','w')
fh.write(json.dumps(obj_json))
fh.close()
print json.dumps(obj_json)

os.system('sudo ifconfig eth0')
os.system('sudo ifconfig eth0 ' + _IP_BUFFER + ' netmask 255.255.255.0')
os.system('sudo route add default gw 192.168.0.1')
os.system('sudo ifconfig eth0 up')

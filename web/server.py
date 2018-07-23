# -*- coding:utf-8 -*-
#encoding=utf-8
import SimpleHTTPServer  
import SocketServer  
import re
import json
import time
import os  
import socket, fcntl, struct 
import sys
import urlparse
import smbus


defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
    
def check_byte(l):
    total_sum = 0
    for c in range(0,len(l)):
        total_sum = total_sum + l[c]
    value_LI  = total_sum & 0xff
    value_HI  = (total_sum >> 8) & 0xff
    return value_LI,value_HI 
  

  
def get_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
    

G_PATH = os.getcwd()
G_PARENT_PATCH = "/.."
G_HF_CONF_JSON = None
G_ACTION = 0
G_HOST = "192.168.18.1:8000"

def sendUDPMessage(message, port=9099):
    address = ('127.0.0.1', port)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    r_buffer = ""
    time.sleep(0.02)    
    tmBegin = time.time()
    s.sendto(message, address)
    
    while time.time()-tmBegin < 2:
        try:
            data, addr = s.recvfrom(65526)
            r_buffer = r_buffer + data
            json.loads(r_buffer)
            s.close()
            return r_buffer
        except Exception, e:
            pass   
        time.sleep(0.05)
    s.close()  
    return ""
    
    
def htc(m):  
    return chr(int(m.group(1),16))  
  
def urldecode(url):  
    rex=re.compile('%([0-9a-hA-H][0-9a-hA-H])',re.M)  
    return rex.sub(htc,url)
    

def readfile(filename): 
        contents = ""
        try:
                fh = open(G_PATH + filename, 'r') 
                contents = fh.read()
                fh.close() 
        except Exception, e:
                print 'readfile error:' + str(e)
                pass
        return contents
        
def savefile(filename, contents, ty='a'): 
        try:
            fh = open(G_PATH + filename, ty) 
            fh.write(contents + "\n") 
        except Exception, e:
            print 'savefile error:' + str(e)
        fh.close() 

    
def get_hf_conf():
        obj_json = None
        jsontext_config = readfile(G_PARENT_PATCH + "/hf.conf")
        #print "jsontext_config",jsontext_config
        try:
            if jsontext_config != "":
                obj_json = json.loads(jsontext_config)
                savefile(G_PARENT_PATCH + "/hf.conf", json.dumps(obj_json), "w")  
                return obj_json
        except Exception, e:
                print 'get_hf_conf error:' + str(e) 
                
                
def qs(url):
    query = urlparse.urlparse(url).query
    return dict([(k,v[0]) for k,v in urlparse.parse_qs(query).items()])  
    
def do_alert():
    obj = {"action":"sensor_write", "data":{"BELL":1,"OUT1":1,"OUT2":1}}
    sendUDPMessage(json.dumps(obj))
    time.sleep(1)
    obj = {"action":"sensor_write", "data":{"BELL":0,"OUT1":0,"OUT2":0}}
    sendUDPMessage(json.dumps(obj))
    time.sleep(1)
    obj = {"action":"sensor_write", "data":{"BELL":1,"OUT1":1,"OUT2":1}}
    sendUDPMessage(json.dumps(obj))
    time.sleep(1)
    obj = {"action":"sensor_write", "data":{"BELL":0,"OUT1":0,"OUT2":0}}
    sendUDPMessage(json.dumps(obj)) 
    time.sleep(1)
    obj = {"action":"sensor_write", "data":{"BELL":1,"OUT1":1,"OUT2":1}}
    sendUDPMessage(json.dumps(obj)) 
    time.sleep(1)
    obj = {"action":"sensor_write", "data":{"BELL":0,"OUT1":0,"OUT2":0}}
    sendUDPMessage(json.dumps(obj))
        
class SETHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):  
    _IP_BUFFER = [0]*11
    global G_HF_CONF_JSON
    def create_index_html(self):
        #print "#########################3create_index_html####################"
        localIP = get_ip("eth0")
        handler = file("index.html", "r")
        text = ""
        for line in handler:
            text = text + line
        text = text.replace("{value_ip}", str(localIP))
        text = text.replace("{value_host}", "http://" + G_HOST)
        
        G_HF_CONF_JSON = get_hf_conf()
        #print "##############G_HF_CONF_JSON",G_HF_CONF_JSON

        for k in G_HF_CONF_JSON:
            #print "{value_" + k + "}"," ==> ", str(G_HF_CONF_JSON[k])
            text = text.replace("{value_" + k + "}", str(G_HF_CONF_JSON[k]))
            pass
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(text)  #get or post request

        
    def create_test_html(self):
        #print "#########################create_test_html####################"

        handler = file("test.html", "r")
        text = ""
        for line in handler:
            text = text + line
        text = text.replace("{value_host}", "http://" + G_HOST)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(text)
        print "create_test_html",text

    def do_GET(self):  
        #print "#########################do_GET####################"
        global G_HOST
        G_HOST = self.headers.getheader('host')
        print "GET"
        #print self.path
        param = qs(self.path)
        print "do_GET",param
            
        if "A" in param.keys():
            if param["A"] == "TEST":
                #show test page
                self.create_test_html()
                return
                
            if param["A"] == "CHG" or param["A"] == "DISCHG" or param["A"] == "RESET" or param["A"] == "ALERT":
                
                if param["A"]=="ALERT":
                    do_alert()
                    
                if param["A"]=="RESET":
                    obj = {"action":"reset"}
                    sendUDPMessage(json.dumps(obj), 9088)

                if param["A"]=="CHG":
                    try:
                        voltage = param["V"]
                        current = param["C"]
                        obj = {"process": [{"station": 2,"time": "60","current": current ,"upperVoltage": voltage, "lowerVoltage": "0" }, {"station": 6}] , "action": "start"}
                        print sendUDPMessage(json.dumps(obj), 9088)
                    except Exception, e:
                        print e
                        pass
                        
                if param["A"]=="DISCHG":
                    try:
                        voltage = param["V"]
                        current = param["C"]
                        obj = {"process": [{"station": 4,"time": "60","current": current ,"upperVoltage": voltage, "lowerVoltage": "0" }, {"station": 6}] , "action": "start"}
                        print sendUDPMessage(json.dumps(obj), 9088)
                    except Exception, e:
                        print e
                        pass
                    
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()               
                return
                
            if param["A"] == "UNIT_DATA":
                #{"action":"unit_stat_readall"}
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                obj = {"action":"unit_stat_readall"}
                ret = sendUDPMessage(json.dumps(obj), 9088)
                self.wfile.write(ret)
                return
                
            if param["A"] == "BATTERY_DATA":
                #{"action":"battery_data"}
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                obj = {"action":"battery_data"}
                ret = sendUDPMessage(json.dumps(obj), 9088)
                self.wfile.write(ret)
                return
        else:    
            self.create_index_html()
        pass
     
    def do_POST(self):  
        print "#########################do_POST####################"
        print "POST"  
        print self.headers;  
        
        length = int(self.headers.getheader('content-length'))  
        qs = self.rfile.read(length)
        url=urldecode(qs)
        print "############print url############",url

        if length>0:
            print "#get the message from html"
            params = url.split("&")#get the message from html
            print "#get the message from html"
            #read document from the hf.conf
            #os.system('python ~/hf_formation/run_setnetwork.py')
            self._IP_BUFFER = None
            G_HF_CONF_JSON = get_hf_conf()
            for p in params:
                agvs = p.split("=")
                G_HF_CONF_JSON[agvs[0]] = agvs[1]
                if(agvs[0] == "ip"):
                    self._IP_BUFFER = [int(i) for i in agvs[1].split(".")]
                    self._IP_BUFFER.append(0xaa)
                    for i in range(1,6):
                        self._IP_BUFFER.append(i)
                        
                    value_LI,value_HI = check_byte(self._IP_BUFFER[0:10])
                    self._IP_BUFFER.append(value_LI)
                    self._IP_BUFFER.append(value_HI)
                    print self._IP_BUFFER
                    
                    bus = smbus.SMBus(1)
                    for j in range(0,10):
                        
                        bus.write_i2c_block_data(0x30, 12,self._IP_BUFFER)
                        time.sleep(0.2)
                        dat = [0] *12
                        dat = bus.read_i2c_block_data(0x30,11,12)
                        print "dat:",dat
                        time.sleep(0.1)
                        if dat[10] != self._IP_BUFFER[10]  or  dat[11] != self._IP_BUFFER[11]:
                            time.sleep(0.1)
                            print "i2c write erro!!"
                        else:
                            break

                    os.system('python ~/hf_formation/run_setnetwork.py')
                
            print "G_HF_CONF_JSON:",G_HF_CONF_JSON
            pass
        self.send_response(302)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Location", G_HOST + "?t=" + str(time.time()))
        self.end_headers()
    
        #self.create_index_html()  
          
Handler = SETHandler  
PORT = 8000
#G_HF_CONF_JSON = get_hf_conf()
print "G_HF_CONF_JSON",G_HF_CONF_JSON
#os.system('python ~/hf_formation/run_setnetwork.py')
#print "done the run_setnetwork.py"
httpd = SocketServer.TCPServer(("", PORT), Handler)  
print "serving at port", PORT  
httpd.serve_forever()  


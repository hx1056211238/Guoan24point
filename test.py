data = "013F0200#0100010101010100,64"
tmp = data.split(',')
ret_len = int(tmp[-1]) + 1 #received lenghth
bn = 0
print "tmp:",tmp[:-1]
c = tmp[:-1]
for c in tmp[:-1]:
    #print "recv command: " + c
    d = c.split('#')
    print "d:",d
    print  "d1:",d[0][:4]
    for i in range(0, len(d[1]),2):
        print "dat:",chr(int(d[1][i:i+2], 16))
    
    s = ''.join(chr(int(d[1][i:i+2], 16)) for i in range(0, len(d[1]),2))
    print "s:",s
    bn = int(int(d[0][:4], 16) >> 5)
    print "bn:",bn
    
    
s = "010101010001010001"    
i=0

for i in range(0, len(s)/16):
    ret_buffer = str(i) + "#"+ s[i*16:i*16+16] +",0" #this place send write meassage
    print "ret_buffer:",ret_buffer
    
i=i+1
ret_buffer = None
if len(s)%16>0:
    k = 16-len(s)%16
    print "k:",k
    print "dat:",s[1:]
    ret_buffer1 = "013F030" + str(len(s)/16) + "#"+ s[(i*16):] + "0"*k +",8"
    print "ret_buffer1:",ret_buffer1
        
			
			
			
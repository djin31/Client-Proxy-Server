import socket,sys  
 
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         


inputfile =  open(sys.argv[1],'rb')
urls = inputfile.readlines()
data = urls[0].strip()
address,port = (urls[1].strip()).split(" ")
for i in xrange(2,len(urls)):
	data+="," + urls[i].strip()

s.connect((address, int(port)))
print "Socket Created to: address",address,"port ",port
if len(data)>8192:
	print "Too much path data, server can't process"
	print "If need to transmit more data then increase buffer size on server side"
	sys.exit()
s.send(data)
outputfile = open(urls[0].strip(),'wb')
out_data = s.recv(1024) 
print "out_data"
while out_data:
	outputfile.write(out_data)
	out_data = s.recv(1024)
print "received data"

s.close()      

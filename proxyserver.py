from threading import *
import socket,sys,time

listening_port = int(sys.argv[1])

#Assuming that the path data given to client as input would not exceed 8192 bytes
#If more than that, then change the max_buffer_size
max_buffer_size = 8192
max_connections = 5

def transfer(connection,address):
	data = connection.recv(max_buffer_size)
	urls = data.split(",")
	if len(urls)>1:
		next_hop_ip,next_hop_port = urls[1].split(" ")
		try:
			s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s2.connect((next_hop_ip,int(next_hop_port)))
			s2.setblocking(1)
			s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Keep socket open for other connections
			#s2.settimeout(60.0)												#put a time out for testing purposes, comment this out if you want to keep servers idle for longer durations
			#time.sleep(1)
			hop_data=urls[0]
			print urls
			for i in urls[2:]:
				hop_data+=","+i
			s2.send(hop_data)

			file_data = s2.recv(1024)
			while file_data:
				connection.send(file_data)
				file_data = s2.recv(1024)
			s2.close()
			connection.close()

		except Exception as e:
			print str(e)
			print "Problem connecting to the server"
			sys.exit()
	else:
		f = open(urls[0],'rb')
		file_data = f.read(1024)
		while file_data:
			connection.send(file_data)
			file_data=f.read(1024)
		connection.close()
		print "Connection closed to",address


try:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(('',listening_port))
	s.setblocking(1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Keep socket open for other connections
	#s.settimeout(60.0)										#put a time out for testing purposes, comment this out if you want to keep servers idle for longer durations
	#time.sleep(1)
	print "Socket Created and Binded"
	s.listen(max_connections)
except Exception as e:
	print str(e)
	print "Unable to create Socket"
	sys.exit()

while True:
	try:
		connection,address = s.accept()
		print "Connection request from",address
		concurr= Thread(target=transfer,args=(connection,address))
		concurr.setDaemon(True)
		concurr.start()
	except Exception as e:
		s.close()
		print str(e)
		print "Server shutting down"
		sys.exit()

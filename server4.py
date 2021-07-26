import socket
import sys
import ipaddress
import select
import queue
import signal

def signal_handler(signal,frame):
	print("")
	print("closing the server........")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


#create a socket
skt = socket.socket()
skt.setblocking(0)
host = str(ipaddress.ip_address(sys.argv[1]))                    # Get local machine name
port = int(sys.argv[2])


skt.bind((host, port)) 			 # Bind to the port
skt.listen(2) 					 #listen to max 2 clients

#sockets from which we expect to read and write  i.e inputs and outputs
inp = [skt]	 
op = [ ]

#outgoing msgs queue
msg_q = {}

while inp:
	readable, writable, exceptional = select.select(inp,op,inp)

	for s in readable:
		if s is skt:
			cln, addr = s.accept()      #readable server accepts the connection
			print("server is connected to : ", addr)
			cln.setblocking(0)
			inp.append(cln)
			msg_q[cln] = queue.Queue()		#the client gets a queue for data to be sent

		else:
			equation = s.recv(1024).decode()
			if equation:
				print("")
				print("received " + str(equation) + " from " ,s.getpeername())
				
				msg_q[s].put(equation)

				if s not in op:
					op.append(s)
				else:
					#stop listening to the client
					if s in op:
						op.remove(s)
					inp.remove(s)
					s.close()
					#remove msg from queue
					del msg_q[s]


	for s in writable:
		try:
			next_msg = msg_q[s].get_nowait()
		except queue.Empty:
			op.remove(s)
			
		else:
			print("sending " + str(equation) +" to ",s.getpeername())
			s.send(next_msg.encode())



	for s in exceptional:
		print("handling exceptional conditions for ",s.getpeername())
		#stop listening
		inp.remove(s)
		if s in op:
			op.remove(s)
		s.close()
		#delete msg from queue
		del msg_q[s]

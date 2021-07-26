import socket
import sys
import ipaddress
import select
import queue
import signal

#signal handling
def signal_handler(signal,frame):
	print("")
	print("closing the server.......")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


#create a socket
skt = socket.socket()
skt.setblocking(0)
host = str(ipaddress.ip_address(sys.argv[1]))                    # Get local machine name
port = int(sys.argv[2])


skt.bind((host, port)) 			 # Bind to the port
skt.listen(3) 					 #listen to max 3 clients

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
			print("")
			cln.setblocking(0)
			inp.append(cln)
			msg_q[cln] = queue.Queue()		#the client gets a queue for data to be sent

		else:
			try:
				equation = s.recv(1024).decode()
				if equation:
					print("")
					print("received " + str(equation) + " from " ,s.getpeername())
					print("evaluating the answer...")
					result = eval(equation)
					#cln.send(str(result).encode())
					msg_q[s].put(result)
					if s not in op:
						op.append(s)

				else:
					if s in op:
						op.remove(s)
					inp.remove(s)
					s.close()
					#remove msg from queue
					del msg_q[s]

			except (ZeroDivisionError):
				cln.send("ZeroDiv".encode())
				if s not in op:
					op.append(s)

			except (ArithmeticError):
				cln.send("SyntaxError".encode())
				if s not in op:
					op.append(s)
			except (SyntaxError):
				cln.send("SyntaxError".encode())
				if s not in op:
					op.append(s)


	for s in writable:
		try:
			next_msg = msg_q[s].get_nowait()
		except queue.Empty:
			op.remove(s)
		else:
			print("sending " + str(result) +" to ",s.getpeername())
			print("answer sent..!!")
			s.send(str(next_msg).encode())



	for s in exceptional:
		print("handling exceptional conditions for ",s.getpeername())
		inp.remove(s)
		if s in op:
			op.remove(s)
		s.close()
		#delete msg from queue
		del msg_q[s]

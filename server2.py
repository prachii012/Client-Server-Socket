import socket
import os
import sys
import ipaddress
from threading import Thread
import signal

def signal_handler(signal,frame):
	print("")
	print("closing the server.......")
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


skt = socket.socket()
host = str(ipaddress.ip_address(sys.argv[1]))                    # Get local machine name
port = int(sys.argv[2])
threads = []


skt.bind((host, port))				#bind to the port
print("server is connected")
print("waiting for client connection...")


class thread(Thread):
	def __init__(self,ip,port):
		Thread.__init__(self)
		self.ip=ip
		self.port = port
		print("new connection from a client ", addr)
		print("\n")

	def run(self):
		while True:
			try:
				equation = cln.recv(1024).decode()
				print("expression recieved from ", addr ," : ", equation)
				print("evaluating the answer....")
				result = eval(equation)
				print("answer sent...!")
				cln.send(str(result).encode())
			
			except (ZeroDivisionError):
				cln.send("ZeroDiv".encode())
			except (ArithmeticError):
				cln.send("SyntaxError".encode())
			except (SyntaxError):
				cln.send("SyntaxError".encode())

				cln.close()

while(True): 
	skt.listen(5)
	cln, addr = skt.accept()
	newthread = thread(host,port)
	newthread.start()
	threads.append(newthread)

for t in threads:
	t.join()

skt.close()
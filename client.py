import sys
import socket
import ipaddress
import signal

#signal handling
def signal_handler(signal,frame):
	print("")
	print("disconnecting.....")
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

skt = socket.socket()		#create a socket
try:
	host = str(ipaddress.ip_address(sys.argv[1]))
	port = int(sys.argv[2])
	skt.connect((host,port))		#connect the host to server
	print("connected to server")

	#when connected perform this
	while(True):
		a = input("enter the expression: ")
		skt.send(a.encode())
		result = skt.recv(1024).decode()
		
		print("evaluating your answer...")

		if result == "ZeroDiv":
			print("division by zero is not allowed")
		elif result == "SyntaxError":
			print("enter a valid expression")
		elif result == "NameError":
			print("atleast 2 operands needed")
		else:
			print("answer recieved from the server is ", result)

		print("you are still connected to the server")
		print("")

	skt.close()		#close the socket

except (IndexError, ValueError):
	print("connection not established")

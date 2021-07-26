import socket
import sys
import ipaddress
import signal

#signal handling
def signal_handler(signal,frame):
     print("")
     print("closing the server.......")
     sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#create a socket object
skt = socket.socket() 	  		
#get loacal machine name
host = str(ipaddress.ip_address(sys.argv[1]))                    
port = int(sys.argv[2])


skt.bind((host, port)) 			 # Bind to the port
skt.listen(1) 			         # Now wait for client connection. 1 at a time

print("Server is connected")

#when server is connected, perform this
while(True):
     cln, addr = skt.accept() 		# Establish connection with client.
     print("server is connected to ", addr)

     while True:
          try:
               equation=cln.recv(1024).decode()        #recieve the equation from client
               if not equation:
                    break
               print("")
               print("expression recieved from client : ", equation)                    
               print("evaluating the answer....")
               result = eval(equation)            #evaluate the equation
               print("answer sent..!")
               cln.send(str(result).encode())     #send the answer to the client
               
          except(ZeroDivisionError):
               cln.send("ZeroDiv".encode())
               print("OOPSSS.!! Some error")
               print("error sent to the client")
          except (ArithmeticError):
               cln.send("SyntaxError".encode())
               print("OOPSSS.!! Some error")
               print("error sent to the client")
          except (SyntaxError):
               cln.send("SyntaxError".encode())
               print("OOPSSS.!! Some error")
               print("error sent to the client")
          

     cln.close() 			# Close the connection.

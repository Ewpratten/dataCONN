import socket
from collections import deque

class Server(object):
	""" dataCONN server """
	def __init__(self, listen="0.0.0.0", port=8088, handout=range(8089,8120)):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((listen, port))
		self.busy_ports = []
		self.connections = {}
		self.handout_range = deque(handout)
		self.seen = []
		self.interface = listen
	
	def __send(self, message, server, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(message.encode(), (server, port))
	
	def __genLUT(self):
		self.commandLUT = {
			"request": self.__connect
		}
	
	def __connect(self, arg, port, addr):
		ip, _ = addr
		s_port = list(set(self.handout_range) - set(self.busy_ports))[0]
		self.connections[ip] = {"c_port": port, "s_port": s_port}
		self.__send("accepting on "+ str(s_port), ip, int(port))
		self.busy_ports.append(s_port)
		#listen
		self.__connectedComs(ip, port, s_port)
	
	def __connectedComs(self, ip, port, lport):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self.interface, lport))
		
		while True:
			data, addr = self.sock.recvfrom(1024)
			data = data.decode()
			
			payload = self.callback(data, addr)
			if payload != None:
				self.__send(payload, ip, int(port))
	
	def __handleNewConn(self, data, addr):
		data = data.decode().strip()
		message = data.split(" ")
		# deal with pings
		if len(message) == 1:
			if message[0] == "ping":
				self.seen.append(addr)
				return
		
		# parse message
		request = message[0]
		arg     = message[1]
		port    = message[2]
		
		print(message)
		# Run command
		# try:
		self.commandLUT[request](arg, port, addr)
		# except:
			# print("Invalid command sent by "+ str(addr))
		
	
	def listen(self, callback):
		self.callback = callback
		# Generate the look up table of commands
		self.__genLUT()
		while True:
			data, addr = self.sock.recvfrom(1024)
			self.__handleNewConn(data, addr)

def testCall(data, addr):
	print(data)
	return data
if __name__ == "__main__":
	print("Starting Server")
	s = Server()
	s.listen(testCall)
import socket

class Client(object):
	""" dataCONN client """
	def __init__(self, return_port=8087):
		self.return_port = return_port
	
	def __send(self, message, server, port=8088):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(message.encode(), (server, port))
	
	
	def connect(self, server, callback, port=8088):
		self.server = server
		# set up listener for server response
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(("0.0.0.0", self.return_port))
		
		# send connection request to server
		self.__send("ping", server, port)
		self.__send("request connect "+ str(self.return_port), server, port)
		
		# listen for a response
		while True:
			data, addr = self.sock.recvfrom(1024)
			print(data.decode())
			response = data.decode().split(" ")
			if response[0] == "accepting":
				server_port = response[2]
				break
		print("Server is accepting a connection on port "+ str(server_port))
		ip, _ = addr
		self.server_port = server_port
		
		# while True:
		# 	data, addr = sock.recvfrom(1024)
		# 	data = data.decode()
		# 	callback(data, addr)
	
	def send(self, message):
		self.__send(message, self.server, int(self.server_port))
	
	def recv(self):
		data, addr = self.sock.recvfrom(1024)
		data = data.decode()
		return data

def shell(data, addr):
	print(data)

if __name__ == "__main__":
	c = Client()
	c.connect("127.0.0.1", shell)
	
	while True:
		print("Server Shell")
		data = input(">")
		c.send(data)
		print(c.recv())
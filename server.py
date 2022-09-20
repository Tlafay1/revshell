import socket
from outputs import Output

HEAD = 64

# The class that handles server operations. Maybe written in C one day ?
# This one is probably the most stable so far, except eventually some more
# exception handling.

class Server:
	def __init__(self, ip='0.0.0.0', port=1234):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((ip, port))
		self.s.listen()
		Output.success(f"Listening on {ip}:{port} ...")

	def accept(self):
		self.client_socket, client_ip = self.s.accept()
		Output.success(f"Connection from {client_ip[0]}:{client_ip[1]}")

	def send_header(self, length):
		msg_size = str(length).encode()
		msg_size += b' ' * (HEAD - len(msg_size))
		try:
			self.client_socket.sendall(msg_size)
		except:
			Output.error("Failed to transfer data on socket.")
			Output.error("The shell might be unstable !")

	def get_header(self):
		int(self.recvall(HEAD))

	def send(self, msg):
		msg = msg.encode()
		if len(str(len(msg))) > HEAD:
			Output.error("Message too long.")
			Output.error("The last message hasn't been sent")
		try:
			self.send_header(len(msg))
			self.client_socket.sendall(msg)
		except:
			Output.error("Failed to transfer data on socket.")
			Output.error("The shell might be unstable !")

	def send_bytes(self, msg):
		msg = msg
		if len(str(len(msg))) > HEAD:
			Output.error("Message too long.")
			Output.error("The last message hasn't been sent")
		try:
			self.send_header(len(msg))
			self.client_socket.sendall(msg)
		except:
			Output.error("Failed to transfer data on socket.")
			Output.error("The shell might be unstable !")

	def recvall(self, size):
		ret = b''
		while len(ret) < size:
			ret += self.client_socket.recv(size)
		return ret.decode()
	
	def recv(self):
		msg_size = int(self.recvall(HEAD))
		return self.recvall(msg_size)

	def recvall_bytes(self, size):
		ret = b''
		while len(ret) < size:
			ret += self.client_socket.recv(size)
		print(f"Expected {size} bytes and received {len(ret)}")
		return ret

	def recv_bytes(self):
		msg_size = int(self.recvall_bytes(HEAD))
		return self.recvall_bytes(msg_size)

	def send_raw(self, msg):
		self.client_socket.sendall(msg.encode())

	def recv_raw(self, size):
		return(self.client_socket.recv(size).decode())

	def get_client_socket(self):
		return self.client_socket

	def __del__(self):
		try:
			self.client_socket.close()
		except:
			pass
		self.s.close()
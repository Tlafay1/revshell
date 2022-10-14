import socket
from outputs import Output

HEAD = 64


class Client:
	def __init__(self, ip, port):
		self.s = socket.socket()
		try:
			self.s.connect((ip, port))
		except (socket.error):
			Output.error("Couldn't connect to host.")
			exit(1)

	def send_header(self, length):
		msg_size = str(length).encode()
		msg_size += b' ' * (HEAD - len(msg_size))
		try:
			self.s.sendall(msg_size)
		except socket.error:
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
			self.s.sendall(msg)
		except socket.error:
			Output.error("Failed to transfer data on socket.")
			Output.error("The shell might be unstable !")

	def send_bytes(self, msg):
		if len(str(len(msg))) > HEAD:
			Output.error("Message too long.")
			Output.error("The last message hasn't been sent")
		try:
			self.send_header(len(msg))
			self.s.sendall(msg)
		except socket.error:
			pass
			Output.error("Failed to transfer data on socket.")
			Output.error("The shell might be unstable !")

	def recvall(self, size):
		ret = b''
		while len(ret) < size:
			ret += self.s.recv(size)
		return ret.decode()

	def recv(self):
		msg_size = int(self.recvall(HEAD))
		return self.recvall(msg_size)

	def recvall_bytes(self, size):
		ret = b''
		while len(ret) < size:
			ret += self.s.recv(size)
		return ret

	def recv_bytes(self):
		msg_size = int(self.recvall_bytes(HEAD))
		return self.recvall_bytes(msg_size)

	def send_raw(self, msg):
		self.s.sendall(msg.encode())

	def recv_raw(self, size):
		return(self.s.recv(size).decode())

	def get_client_socket(self):
		return self.s

	def __del__(self):
		self.s.close()

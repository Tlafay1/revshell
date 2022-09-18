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
			self.s.sendall(msg)
		except:
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

	def send_file(self, file):
		try:
			file_size = os.stat(file).st_size
		except FileNotFoundError:
			msg_size = str(1).encode()
			msg_size += b' ' * (HEAD - len(msg_size))
			self.s.send('0'.encode())
			return
		self.s.send((str(file_size) + '\n').encode())
		with open(file, 'r') as f:
			while file_size > 0:
				data = f.readline()
				file_size -= len(data)
				self.s.sendall(data.encode())

	def recv_file(self, path):
		file_size = int(self.recvall(HEAD))
		if file_size == 0:
			return
		with open(path, 'w') as f:
			data = self.recvall(file_size)
			f.write(data)

	def send_raw(self, msg):
		self.s.sendall(msg.encode())

	def recv_raw(self, size):
		return(self.s.recv(size).decode())

	def get_client_socket(self):
		return self.s

	def __del__(self):
		self.s.close()
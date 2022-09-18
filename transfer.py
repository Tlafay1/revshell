import socket
import os

HEAD = 64

# On it's way !
class FileTransfer:
	def __init__(self, server):
		self.server = server

	def send(self, file):
		if not os.path.isfile(file):
			self.server.send('')
			return 1
		file_size = os.stat(file).st_size
		self.server.send_header(file_size)
		with open(file, 'r') as f:
			for line in f:
				self.server.send_raw(line)
		return 0

	def receive(self, path):
		data = self.server.recv()
		if len(data) == 0:
			return
		with open(path, 'w') as f:
			f.write(data)

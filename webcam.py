import struct
# import cv2
import pickle
import imageio
import matplotlib.pyplot as plt
import numpy as np
import time

# Still not very stable, need a way to stop
# that thing and handle exceptions in case client
# SIGINTs

class Webcam:
	def __init__(self, server):
		self.server = server

	def receive(self):
		while True:
			frame_data = self.server.recv_bytes()
			frame = pickle.loads(frame_data)
			plt.imshow(frame)
			plt.show(block=False)
			plt.pause(1 / 30)
			plt.close()

# Capture video with webcam

class VideoStream:
	def __init__(self, client):
		self.client = client

	def send(self):
		camera = imageio.get_reader("<video0>")
		meta = camera.get_meta_data()
		while True:
			frame = camera.get_next_data()
			a = pickle.dumps(frame)
			self.client.send_bytes(a)
			# plt.imshow(frame)
			# plt.show(block=False)
			# plt.pause(delay)
			# plt.close()
		camera.close()

		# while(1):
			# img, frame = vid.read()
			# a = pickle.dumps(frame)
			# message = struct.pack("Q", len(a)) + a
			# self.s.sendall(message)


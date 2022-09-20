import struct
import pickle
import imageio
import matplotlib.pyplot as plt
import time
# import tkinter as tk, threading
# from PIL import Image, ImageTk

# I got a cross-platform camera ! I still need to create a way to
# stop the loop on 

class Webcam:
	def __init__(self, server):
		self.server = server

	def receive(self):
		while True:
			frame_data = self.server.recv_bytes()
			self.server.send("received")
			frame = pickle.loads(frame_data)
			plt.imshow(frame)
			plt.show(block=False)
			plt.pause(1 / 30)
			plt.close()
			# root = tk.Tk()
			# my_label = tk.Label(root)
			# my_label.pack()
			# thread = threading.Thread(target=stream, args=(my_label,))
			# thread.daemon = 1
			# thread.start()
			# root.mainloop()

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
			received = self.client.recv()
			time.sleep(1 / 30)
		camera.close()


import struct
import pickle
import imageio
import time
from outputs import Output
import visvis as vv

# I got a cross-platform camera ! I still need to create a way to
# stop the loop on 

class Webcam:
	def __init__(self, server):
		self.server = server

	def receive(self):
		status = self.server.recv()
		if status == "ABORT":
			Output.error('No working camera found')
			return

		frame_data = self.server.recv_bytes()
		self.server.send("received")
		frame = pickle.loads(frame_data)
		vv.axis('off')
		t = vv.imshow(frame, clim=(0, 255))
		
		try:
			while True:
				im_data = self.server.recv_bytes()
				self.server.send("received")
				im = pickle.loads(im_data)
				vv.processEvents()
				t.SetData(im)
		except KeyboardInterrupt:
			self.server.send("STOP")
			t.Destroy()
			self.server.recv_bytes()

# Capture video with webcam

class VideoStream:
	def __init__(self, client):
		self.client = client

	def send(self):
		try:
			camera = imageio.get_reader("<video0>")
			self.client.send("OK")
		except IndexError:
			self.client.send("ABORT")
			return

		frame = camera.get_next_data()
		a = pickle.dumps(frame)
		self.client.send_bytes(a)
		received = self.client.recv()

		for im in camera:
			a = pickle.dumps(im)
			self.client.send_bytes(a)
			received = self.client.recv()
			if (received == "STOP"):
				break
			time.sleep(1 / 30)
		camera.close()


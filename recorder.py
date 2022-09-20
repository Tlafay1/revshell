import pyaudio

class Recorder:
	def __init__(self, client):
		self.audio = pyaudio.PyAudio()
		self.client = client

	def record(self):
		stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
			input=True, frames_per_buffer=1024)

		frame = []

		while True:
			data = stream.read(1024)
			self.client.send_bytes(data)
			if self.client.recv() == "STOP":
				break
		stream.stop_stream()
		stream.close()

	def __del__(self):
		self.audio.terminate()

class Player:
	def __init__(self, server):
		self.audio = pyaudio.PyAudio()
		self.server = server

	def play(self):
		stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
			output=True, frames_per_buffer=1024)

		try:
			while True:
				data = self.server.recv_bytes()
				self.server.send('received')
				stream.write(data)
		except KeyboardInterrupt:
			self.server.send('STOP')

		stream.stop_stream()
		stream.close()

	def __del__(self):
		self.audio.terminate()

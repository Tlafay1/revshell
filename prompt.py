import readline

class InteractivePrompt:

	def __init__(self):
		self.options = sorted(['shell', 'webcam', 'download', 'upload', 'exit'])
		return

	def input(self, msg):
		readline.set_completer(self.complete)
		readline.parse_and_bind('tab: complete')
		try:
			cmd = '\n'
			while cmd == '\n':
				cmd = input(msg)
		except EOFError:
			return None

		return cmd.strip()

	def complete(self, text, state):
		response = None
		if state == 0:
			if text:
				self.matches = [s 
				for s in self.options
				if s and s.startswith(text)]
			else:
				self.matches = self.options[:]
		try:
			response = self.matches[state]
		except IndexError:
			response = None
		return response
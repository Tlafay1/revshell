import readline
import os

class InteractivePrompt:

	def __init__(self):
		self.commands = sorted(['shell', 'webcam', 'download', 'upload', 'exit'])
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

	def get_cur_before(self):
		idx = readline.get_begidx()
		full = readline.get_line_buffer()
		return full[:idx]

	# def get_current(self):
	# 	return readline.get_line_buffer()[readline.get_begidx():readline.get_endidx()]

	def complete(self, text, state):
		# last_slash = text.rfind('/')
		# if last_slash == -1:
		# 	path = text
		# else:
		# 	path = text[:last_slash]
		# 	text = text[last_slash + 1:]
		# if text:
		# 	server_files = os.listdir(path)
		# else:
		server_files = os.listdir('.')
		if len(self.get_cur_before().split(" ")) <= 1:
			results = [x + " " for x in self.commands if x.startswith(text)] + [None]
		else:
			results = [x + " " for x in server_files if x.startswith(text)] + [None]
		return results[state]


# if text:
# 	text = text.substr(0, text.rfind('/'))
# 	server_files = os.listdir(text)
# else:
# 	server_files = os.listdir('.')
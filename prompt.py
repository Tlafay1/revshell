import readline
import os

class InteractivePrompt:

	def __init__(self):
		readline.set_completer_delims(readline.get_completer_delims().replace('~', ''))
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

	def complete(self, text, state):
		buff_len = len(self.get_cur_before().split(" "))

		match buff_len:
			case 0:
				results = [x + " " for x in self.commands if x.startswith(text)] + [None]
			case 1:
				results = [x + " " for x in self.commands if x.startswith(text)] + [None]
			case 2:
				current_path = self.get_cur_before().split(" ")[-1]
				path = os.path.dirname(current_path) if os.path.dirname(current_path) else '.'
				server_files = [os.path.basename(x) for x in os.listdir(path)]
				server_files = [x + '/' if os.path.isdir(path + '/' + x) else x for x in server_files]
				results = [x for x in server_files if x.startswith(text)] + [None]
			case 3:
				current_path = self.get_cur_before().split(" ")[-1]
				path = os.path.dirname(current_path) if os.path.dirname(current_path) else '.'
				server_files = [os.path.basename(x) for x in os.listdir(path)]
				server_files = [x + '/' if os.path.isdir(path + '/' + x) else x for x in server_files]
				results = [x for x in server_files if x.startswith(text)] + [None]
			case _:
				return None
		return results[state]
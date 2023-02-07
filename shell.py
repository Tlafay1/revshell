import time
import signal
import sys
from prompt import readline

# The shell is still not that stable, i still have work to do.
class Shell:
	def __init__(self, server):
		self.server = server

	def listener(self):
		readline.set_completer(None)
		print(readline.get_completer())
		# signal.signal(signal.SIGINT, signal.SIG_IGN)
		cmd = None
		while(True):
			out = self.server.recv_raw(4096)
			if out == '\x00':
				break
			if cmd is not None:
				sys.stdout.write(out.split('\n', 1)[1])
			else:
				sys.stdout.write(out)
			try:
				cmd = input() + '\n'
			except EOFError:
				cmd = '\x04'
				sys.stdout.write('\n')
			self.server.send_raw(cmd)
			if cmd == '\n':
				print(cmd)
			time.sleep(0.01)
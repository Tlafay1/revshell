import time
import signal
import sys

# The shell is still not that stable, i still have work to do.
class Shell:
	def __init__(self, server):
		self.server = server

	def listener(self):
		# signal.signal(signal.SIGINT, signal.SIG_IGN)
		cmd = ''
		while(True):
			out = self.server.recv_raw(4096)
			if cmd:
				sys.stdout.write(out.replace(cmd, ''))
			try:
				cmd = input() + '\n'
			except EOFError:
				print("")
				return
			self.server.send_raw(cmd)
			if cmd == 'exit\n':	
				return
			time.sleep(0.01)
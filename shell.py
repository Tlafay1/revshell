import time
import signal
import sys
from prompt import InteractivePrompt

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
			prompt = InteractivePrompt()
			cmd = prompt.input("")
			self.server.send_raw(cmd + '\n')
			if not cmd or cmd == 'exit':	
				break
			time.sleep(0.01)

		sys.stdout.write(self.server.recv_raw(4096))
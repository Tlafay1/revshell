import colorama

class Output:
	def success(msg):
		print(colorama.Fore.GREEN + '[+] ' + colorama.Style.RESET_ALL + msg)

	def warning(msg):
		print(colorama.Fore.BLUE + '[-] ' + colorama.Style.RESET_ALL + msg)

	def error(msg):
		print(colorama.Fore.RED + '[!] ' + colorama.Style.RESET_ALL + msg)
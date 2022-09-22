from outputs import Output
import urllib.request, urllib.error
import os

class Download:
	def __init(self, client):
		self.client = client

	def get(url, path=None):
		print(path)
		try:
			filename = url.rstrip('/').rsplit('/', 1)[-1].split('#')[0]
			if path:
				if os.isdir(path):
					path = path.rstrip('/') + '/' + filename
			else:
				path = filename
			path, headers = urllib.request.urlretrieve(url=url, filename=path)
			Output.success(f'Successfully downloaded {url}')
			Output.success(f'File is located at {path}')
		except urllib.error.URLError as e:
			Output.error(f'Transfer failed for the following reason: {e}')
		except ValueError as e:
			Output.error(f'Transfer failed for the following reason: {e}')


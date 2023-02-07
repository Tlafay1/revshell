from outputs import Output
import urllib.request, urllib.error
import os
import sys

class Download:
	def __init__(self, client):
		self.client = client

	def get_size():
		meta = urllib2.urlopen(url).info()
		meta_func = meta.getheaders if hasattr(
			meta, 'getheaders') else meta.get_all
		meta_length = meta_func('Content-Length')
		try:
			return int(meta_length[0])
		except:
			return 0

	def kb_to_mb(kb):
		return kb / 1024.0 / 1024.0

	def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
		count = len(it)
		def show(j):
			x = int(size*j/count)
			print(f"{prefix}[{"#"*x}{"."*(size-x)}] {j}/{count}", 
				end='\r', file=out, flush=True)
		show(0)
		for i, item in enumerate(it):
			yield item
			show(i+1)
		print("\n", flush=True, file=out)

	def wget(url, path=None):
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


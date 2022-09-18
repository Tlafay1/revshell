# Well, just copy pasted code from the internet for now

class ScreenStream:

	def __init__(self, client_socket):
		self.client_socket = socket

	def recvall(self, conn, length):
		buf = b''
		while len(buf) < length:
			data = self.client_socket.recv(length - len(buf))
			if not data:
				return data
			buf += data
		return buf

	def stream():
		pygame.init()
		screen = pygame.display.set_mode((WIDTH, HEIGHT))
		clock = pygame.time.Clock()
		watching = True


		try:
			while watching:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						watching = False
						break

				# Retreive the size of the pixels length, the pixels length and pixels
				size_len = int.from_bytes(conn.recv(1), byteorder='big')
				size = int.from_bytes(conn.recv(size_len), byteorder='big')
				pixels = decompress(recvall(conn, size))

	            # Create the Surface from raw pixels
				img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

	            # Display the picture
				screen.blit(img, (0, 0))
				pygame.display.flip()
				clock.tick(60)
		finally:
			print("PIXELS: ", pixels)
			sock.close()
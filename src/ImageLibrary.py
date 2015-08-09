import pygame
import os

class ImageLibrary:
	def __init__(self):
		self.images = {}
	
	def get(self, path):
		img = self.images.get(path, None)
		if img == None:
			real_path = ('images/' + path).replace('\\', '/').replace('//', '/').replace('/', os.sep)
			img = pygame.image.load(real_path).convert_alpha()
			img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
			self.images[path] = img
		return img

IMAGES = ImageLibrary()

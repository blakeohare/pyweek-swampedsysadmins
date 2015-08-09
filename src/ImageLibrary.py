import pygame
import os

_flipped_sprites = {}

for i in range(50):
	for prefix in ['man', 'woman']:
		for n in range(10):
			a, b = 'images/sprites/' + prefix + str(i) + '_', str(n) + '.png'
			_flipped_sprites[a + 'w' + b] = a + 'e' + b

class ImageLibrary:
	def __init__(self):
		self.images = {}
	
	def get(self, path):
		img = self.images.get(path, None)
		if img == None:
			real_path = ('images/' + path).replace('\\', '/').replace('//', '/')
			flipped_image = _flipped_sprites.get(real_path, None)
			real_path = real_path.replace('/', os.sep)
			
			if flipped_image != None:
				img = pygame.image.load(flipped_image).convert_alpha()
				img = pygame.transform.flip(img, True, False)
			else:
				img = pygame.image.load(real_path).convert_alpha()
			actual = pygame.Surface(img.get_size()).convert()
			actual.fill((255, 0, 255))
			actual.blit(img, (0, 0))
			
			img = pygame.transform.scale2x(actual).convert()
			img.set_colorkey((255, 0, 255))
			self.images[path] = img
		return img

IMAGES = ImageLibrary()

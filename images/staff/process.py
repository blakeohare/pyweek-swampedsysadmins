import pygame
import os

def get_template_names():
	output = {}
	for file in os.listdir('.'):
		if file.startswith('template'):
			prefix = file.split('_')[0]
			output[prefix] = True
	values = list(output.keys())
	values.sort()
	return values

_images = {}

def get_image(template, dir, id):
	path = template + '_' + dir + str(id) + '.png'
	img = _images.get(path)
	if img == None:
		if dir == 'w':
			t = get_image(template, 'e', id)
			img = pygame.Surface((16, 32)).convert()
			img.fill((255, 0, 255))
			img.blit(t, (0, 0))
			img = pygame.transform.flip(img, True, False)
		else:
			img = pygame.image.load(path)
		_images[path] = img
	return img
	
pygame.init()
pygame.display.set_mode((400, 400))

templates = get_template_names()
width = 16 * 20 # nsew * (stand + 0123)
height = len(templates) * 32

output = pygame.Surface((width, height)).convert()
output.fill((255, 0, 255))

y = 0

for template in templates:
	x = 0
	for dir in list('nsew'):
		for frame in [0, 1, 0, 2, 0]:
			output.blit(get_image(template, dir, frame), (x, y))
			x += 16
	y += 32

pygame.image.save(output, 'composite.png')

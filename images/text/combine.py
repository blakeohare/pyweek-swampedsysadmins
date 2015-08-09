import pygame

pygame.init()
pygame.display.set_mode((100, 100))

letters = '`abcdefghijklmnopqrstuvwxyz'
filename_overrides = {
	'`': 'unknown',
}

images = {}

for letter in letters:
	filename = filename_overrides.get(letter, letter) + '.png'
	
	images[filename] = pygame.image.load(filename).convert()

final = {}



for key in images.keys():
	raw = images[key]
	width, height = raw.get_size()
	img = pygame.Surface((width + 1, height + 1))
	img.fill((0, 0, 255))
	black = pygame.Surface((width, height)).convert()
	black.fill((0, 255, 0))
	raw.set_colorkey((255, 255, 255)) # white is transparent
	black.blit(raw, (0, 0)) # green background, black letters
	
	temp = pygame.Surface((width, height)).convert()
	temp.fill((0, 255, 0))
	raw.set_colorkey((0, 0, 0)) # black is transparent
	temp.blit(raw, (0, 0)) # green letter, white background
	temp.set_colorkey((255, 255, 255))
	temp2 = pygame.Surface((width, height)).convert()
	temp2.fill((255, 0, 0))
	temp2.blit(temp, (0, 0)) # red background, green letters
	temp2.set_colorkey((0, 255, 0)) # red background
	white = pygame.Surface((width, height)).convert()
	white.fill((255, 255, 255))
	white.blit(temp2, (0, 0)) #red background, white letters
	
	black.set_colorkey((0, 255, 0))
	img.blit(black, (1, 1))
	white.set_colorkey((255, 0, 0))
	img.blit(white, (0, 0))
	
	final[key] = img


width += 2
height += 2

color_lookup = {
	'white': (255, 255, 255),
	'red': (230, 30, 0),
	'green': (0, 180, 40),
	'blue': (40, 100, 255),
	'purple': (200, 40, 200),
	'orange': (255, 128, 0),
	'yellow': (240, 200, 0),
	'gray': (150, 150, 150),
}

colors = color_lookup.keys()[:]
colors.sort()

output = pygame.Surface((width * len(letters), (height * len(colors))))
output.fill((0, 0, 255))
y = 0

def swap_color(image, old, new):
	image2 = image.copy().convert()
	output = pygame.Surface(image2.get_size()).convert()
	output.fill(new)
	image.set_colorkey(old)
	output.blit(image, (0, 0))
	return output

for color in colors:
	x = 0
	for letter in letters:
		filename = filename_overrides.get(letter, letter) + '.png'
		white = final[filename]
		img = swap_color(white, (255, 255, 255), color_lookup[color])
		
		output.blit(img, (x, y))
		x += width
	y += height
pygame.image.save(output, 'composite.png')

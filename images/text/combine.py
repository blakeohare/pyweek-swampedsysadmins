import pygame

LETTERS = '`abcdefghijklmnopqrstuvwxyz.?!/-,\''

BACKGROUND = (255, 0, 255)

def swap_color(image, old, new):
	image2 = image.copy().convert()
	output = pygame.Surface(image2.get_size()).convert()
	output.fill(new)
	image.set_colorkey(old)
	output.blit(image, (0, 0))
	return output

pygame.init()
pygame.display.set_mode((100, 100))

filename_overrides = {
	'`': 'unknown',
	'.': 'period',
	'?': 'question',
	'!': 'bang',
	'/': 'slash',
	'-': 'hyphen',
	',': 'comma',
	"'": 'apostrophe',
}

images = {}

for letter in LETTERS:
	filename = filename_overrides.get(letter, letter) + '.png'
	
	images[filename] = pygame.image.load(filename).convert()

final = {}



for key in images.keys():
	raw = images[key]
	width, height = raw.get_size()
	
	white = swap_color(raw, (255, 255, 255), BACKGROUND) # make background magenta
	white = swap_color(white, (0, 0, 0), (255, 255, 255)) # make foreground white
	black = swap_color(raw, (255, 255, 255), BACKGROUND) # make background magenta
	
	white.set_colorkey(BACKGROUND)
	black.set_colorkey(BACKGROUND)
	
	img = pygame.Surface((width + 1, height + 1)).convert()
	img.fill(BACKGROUND)
	img.blit(black, (1, 1))
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

COLORS = 'white gray red orange yellow green blue purple'.split(' ')

output = pygame.Surface((width * len(LETTERS), (height * len(COLORS))))
output.fill(BACKGROUND)
y = 0

for color in COLORS:
	x = 0
	for letter in LETTERS:
		filename = filename_overrides.get(letter, letter) + '.png'
		white = final[filename]
		img = swap_color(white, (255, 255, 255), color_lookup[color])
		output.blit(img, (x, y))
		x += width
	y += height

pygame.image.save(output, 'composite.png')

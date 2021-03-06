import pygame

def make_grid(width, height):
	output = []
	
	while width > 0:
		width -= 1
		output.append([None] * height)
	return output

def coerce_range(value, lower, upper):
	if value < lower: return lower
	if value > upper: return upper
	return value


def range255(value):
	if value < 0: return 0
	if value > 255: return 255
	return int(value)

_alpha_rects = {}

def draw_alpha_rectangle(screen, x, y, width, height, r, g, b, alpha):
	key = str(width) + ':' + str(height)
	img = _alpha_rects.get(key, None)
	if img == None:
		img = pygame.Surface((width, height)).convert()
	img.fill((r, g, b))
	img.set_alpha(alpha)
	
	screen.blit(img, (x, y))
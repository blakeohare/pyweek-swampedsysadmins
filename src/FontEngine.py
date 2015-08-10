import pygame
from src.ImageLibrary import IMAGES
from src.constants import *
# These values are in the composite image generator
LETTERS = '`abcdefghijklmnopqrstuvwxyz.?!/-,\':0123456789'
COLORS = 'white gray red orange yellow green blue purple'.split(' ')
WIDTH = 7 * 2
HEIGHT = 9 * 2
class FontEngine:
	def __init__(self):
		self.raw_letters_by_color = None
	
	def initialize(self):
		raw = IMAGES.get('text/composite.png')
		self.raw_letters_by_color = {}
		row = 0
		for color in COLORS:
			letters = {}
			self.raw_letters_by_color[color] = letters
			y = row * HEIGHT
			x = 0
			col = 0
			for letter in LETTERS:
				x = col * WIDTH
				col += 1
				img = pygame.Surface((WIDTH, HEIGHT)).convert()
				img.fill((255, 0, 255))
				img.blit(raw, (-x, -y))
				img.set_colorkey((255, 0, 255))
				letters[letter] = img
				if letter.lower() != letter.upper():
					letters[letter.lower()] = img
					letters[letter.upper()] = img
			
			row += 1
		self.space_size = letters['a'].get_width()
		
	def render(self, screen, text, color, x, y):
		if self.raw_letters_by_color == None: self.initialize()
		font = self.raw_letters_by_color[color]
		
		for char in text:
			if char == ' ':
				x += self.space_size
			else:
				char = font.get(char, None)
				if char == None:
					char = font['`']
				screen.blit(char, (x, y))
				x += char.get_width()
		return (x, y + HEIGHT)
		
		
TEXT = FontEngine()
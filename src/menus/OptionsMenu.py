import pygame
from src.MagicPotato import MAGIC_POTATO
from src.constants import *
from src.FontEngine import TEXT

class OptionsMenu:
	def __init__(self, background_scene):
		self.next = None
		self.bg = background_scene
		self.buttons = {
			'full_screen': [0] * 4,
			'sfx_volume': [0] * 4,
			'music_volume': [0] * 4,
			'back': [0] * 4
		}
		self.cursor = (0, 0)
		self.currently_over = None
		
	def update(self, events, mouse_coords):
		self.cursor = mouse_coords
		
		for event in events:
			if event.mousedown:
				if self.currently_over != None:
					self.do_command(self.currently_over)
	
	def do_command(self, id):
		if id == 'full_screen':
			if MAGIC_POTATO.is_full_screen():
				MAGIC_POTATO.set_full_screen(False)
			else: MAGIC_POTATO.set_full_screen(True)
		elif id == 'sfx_volume':
			pass
		elif id == 'music_volume':
			pass
		elif id == 'back':
			# pass
			from src.menus.TitleScene import TitleScene # because top of file didn't work
			self.next = TitleScene()
	
	def render(self, screen, render_counter):
		if self.bg != None:
			self.bg.render(screen, render_counter)
		
		pygame.draw.rect(screen, (40, 40, 40, 100), pygame.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT))
		
		mx, my = self.cursor
		
		y = GAME_HEIGHT // 3
		x = GAME_WIDTH // 4
		
		pygame.draw.rect(screen, (150, 150, 150, 150), pygame.Rect(x * 2, y, 15, 15), 0 if MAGIC_POTATO.is_full_screen() else 1)
		
		current = None
		for option in [
			('Full Screen', 'full_screen'),
			('SFX Volume', 'sfx_volume'),
			('Music Volume', 'music_volume'),
			('Back', 'back')
			]:
			
			label, id = option
			button = self.buttons[id]
			hover = mx > button[0] and mx < button[2] and my > button[1] and my < button[3]
			
			if hover:
				current = id
			
			# if id == 'sfx_volume':
			
			coords = TEXT.render(screen, label, 'white' if hover else 'gray', x, y)
			self.buttons[id] = (x, y, coords[0], coords[1])
			y += 30
		self.currently_over = current
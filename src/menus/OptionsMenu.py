import pygame
from src.MagicPotato import MAGIC_POTATO
from src.constants import *
from src.FontEngine import TEXT
from src.Util import draw_alpha_rectangle

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
		if self.bg != None:
			self.buttons.update({'main_menu': [0] * 4})

		self.cursor = (0, 0)
		self.currently_over = None

		self.sfx_vol = MAGIC_POTATO.get_sound_volume()
		self.music_vol = MAGIC_POTATO.get_music_volume()
		
		self.mouse = 0
		self.over = None
		
	def update(self, events, mouse_coords):
		self.cursor = mouse_coords
		
		for event in events:
			if event.mousedown:
				if self.currently_over in ['full_screen', 'back', 'main_menu']:
					self.do_command(self.currently_over)
				elif self.currently_over in ['sfx_volume', 'music_volume']:
					self.mouse = 1
					self.over = self.currently_over
					self.do_sound(self.over)
			elif event.mouseup:
				self.mouse = 0
				self.over = None
			elif self.mouse == 1:
				self.do_sound(self.over)
	
	def do_command(self, id):
		button = self.buttons[id]
		if id == 'full_screen':
			if MAGIC_POTATO.is_full_screen():
				MAGIC_POTATO.set_full_screen(False)
			else: MAGIC_POTATO.set_full_screen(True)
		elif id == 'back':
			if len(self.buttons) == 5:
				self.next = self.bg
			else: 
				from src.menus.TitleScene import TitleScene # because top of file didn't work
				self.next = TitleScene()
		elif id == 'main_menu':
			from src.menus.TitleScene import TitleScene # because top of file didn't work
			self.next = TitleScene()
	
	def do_sound(self, id):
		width_over_two = GAME_WIDTH // 2
		mx, my = self.cursor
		if id == 'sfx_volume':
			if mx < (width_over_two - 20): pass
			else:
				MAGIC_POTATO.set_sound_volume((mx - width_over_two) // 2)
				self.sfx_vol = MAGIC_POTATO.get_sound_volume()
		elif id == 'music_volume':
			if mx < (width_over_two - 20): pass
			else:
				MAGIC_POTATO.set_music_volume((mx - width_over_two) // 2)
				self.music_vol = MAGIC_POTATO.get_music_volume()

	
	def render(self, screen, render_counter):
		if self.bg != None:
			self.bg.render(screen, render_counter)
		
		if self.bg == None:
			screen.fill((0,0,0))
		
		draw_alpha_rectangle(screen, 0, 0, GAME_WIDTH, GAME_HEIGHT, 40, 40, 40, 200)
		
		mx, my = self.cursor
		
		y = GAME_HEIGHT // 3
		x = GAME_WIDTH // 5
		width_over_two = GAME_WIDTH // 2
		
		current = None
		
		options = [('Full Screen', 'full_screen'),('SFX Volume', 'sfx_volume'),('Music Volume', 'music_volume'),('Back', 'back')]
		if len(self.buttons) == 5: options.append(('Return to Main Menu','main_menu'))
		
		for option in options:
			
			label, id = option
			button = self.buttons[id]
			hover = mx > button[0] and mx < button[2] and my > button[1] and my < button[3]
			
			if self.over == id:
				current = id
				button_color = (255, 255, 255, 255)
				text_color = 'white'
				sfx_color = (255, 0, 0, 255)
				music_color = (0, 255, 0, 255)
			elif hover and (self.over == None):
				current = id
				button_color = (255, 255, 255, 255)
				text_color = 'white'
				sfx_color = (255, 0, 0, 255)
				music_color = (0, 255, 0, 255)
			else:
				button_color = (150, 150, 150, 150)
				text_color = 'gray'
				sfx_color = (180, 0, 0, 180)
				music_color = (0, 180, 0, 180)
			
			coords = TEXT.render(screen, label, text_color, x, y)
			if id == 'full_screen':
				self.buttons[id] = (x, y, width_over_two + 20, coords[1])
				pygame.draw.rect(screen, button_color, pygame.Rect(width_over_two, y, 15, 15), 0 if MAGIC_POTATO.is_full_screen() else 1)
			elif id == 'sfx_volume':
				pygame.draw.line(screen, button_color, (width_over_two, y + 7), (width_over_two + 200, y + 7), 2)
				for i in [18, 36, 55, 73, 91, 109, 127, 145, 164, 182]: # ours go to 11!
					pygame.draw.line(screen, button_color, (width_over_two + i, y + 1), (width_over_two + i, y + 14), 1)
				for i in [0, 200]: # end lines
					pygame.draw.line(screen, button_color, (width_over_two + i, y - 1), (width_over_two + i, y + 16), 1)
				pygame.draw.rect(screen, sfx_color, pygame.Rect(width_over_two + (self.sfx_vol * 2) - 1, y + 3, 3, 10), 0)
				self.buttons[id] = (x, y, width_over_two + 220, coords[1])
			elif id == 'music_volume':
				pygame.draw.line(screen, button_color, (width_over_two, y + 7), (width_over_two + 200, y + 7), 2)
				for i in [18, 36, 55, 73, 91, 109, 127, 145, 164, 182]: # ours go to 11!
					pygame.draw.line(screen, button_color, (width_over_two + i, y + 1), (width_over_two + i, y + 14), 1)
				for i in [0, 200]: # end lines
					pygame.draw.line(screen, button_color, (width_over_two + i, y - 1), (width_over_two + i, y + 16), 1)
				pygame.draw.rect(screen, music_color, pygame.Rect(width_over_two + (self.music_vol * 2) - 1, y + 3, 3, 10), 0)
				self.buttons[id] = (x, y, width_over_two + 220, coords[1])
			else:
				self.buttons[id] = (x, y, coords[0], coords[1])
			y += 30
		self.currently_over = current
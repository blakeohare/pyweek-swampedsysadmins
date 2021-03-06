import pygame
import math

from src.Util import *
from src.PlayBoard import build_office_map
from src.RoomRenderer import ROOM_RENDERER
from src.FontEngine import TEXT

LAVA_PRICE = 50
PLUSH_PRICE = 75
PLANT_PRICE = 100
BEAN_BAG_PRICE = 200
FOOSBALL_PRICE = 500


# 1 - lava lamp 1x1
# 2 - plush 2x1
# 3 - plant 1x1
# 4 - bean bag 2x2
# 5 - foosball 3x2

# 7 - desk N
# 8 - desk S
# 9 - desk E
# 0 - desk W

# builds a map.
# in render, flattens the current cursor onto a copy of the interesting_coords
# when you click, apply the furniture to the model, charge the user, and set .next to an instance of this class with no cursor type
# when there is no cursor type, change the exit text to "Done", otherwise "Cancel"

class PlaceFurnitureMenu:
	def __init__(self, model, return_scene, item_type):
		self.next = None
		self.model = model
		self.return_scene = return_scene
		self.base_interesting_coords = []
		self.grid = build_office_map(None, self.base_interesting_coords, model)
		self.mouse_xy = (0, 0)
		self.item_type = item_type
		self.mouse_down = False
		if self.item_type != None:
			self.item_size = {
				# key: (width, height, effect radius)
				'1': (1, 1, 0),
				'2': (2, 1, 0),
				'3': (1, 1, 0),
				'4': (2, 2, 0),
				'5': (3, 2, 7),
				'6': (1, 1, 7),
				'7': (3, 2, 0),
				'8': (3, 2, 0),
				'9': (2, 3, 0),
				'0': (2, 3, 0),
			}[item_type]
		else:
			self.item_size = (0, 0, 0)
		
		self.width, self.height, self.radius = self.item_size
		self.has_effect = self.radius > 0
		
		
	
	def update(self, events, mouse_xy):
		self.mouse_xy = mouse_xy
		x, y = mouse_xy
		
		self.is_over_done = x < 16 * 5 and y < 24
		
		col = x // 32
		row = y // 32
		
		self.current_valid_coord = None
		
		if self.item_type != None and col >= 8 and col < 19 and row >= 2 and row < 14:
			# check to see if full range is unblocked
			start_x = col
			end_y = row
			end_x = col + self.item_size[0] - 1
			start_y = end_y - self.item_size[1] + 1
			
			available = True
			for x in range(start_x, end_x + 1):
				for y in range(start_y, end_y + 1):
					if x < 19 and y < 14:
						if not self.grid[x][y].passable:
							available = False
							break
					else:
						available = False
			
			if available:
				self.current_valid_coord = (col, row)
		
		for event in events:
			if event.mousedown:
				if self.is_over_done:
					self.next = self.return_scene
				else:
					self.mouse_down = True
			elif event.mouseup and self.mouse_down:
				if self.current_valid_coord != None:
					
					price = {
						'1': LAVA_PRICE,
						'2': PLUSH_PRICE,
						'3': PLANT_PRICE,
						'4': BEAN_BAG_PRICE,
						'5': FOOSBALL_PRICE }[self.item_type]
					
					self.model.budget -= price
					
					
					self.model.furniture.append((self.item_type, self.current_valid_coord[0], self.current_valid_coord[1]))
					self.next = PlaceFurnitureMenu(self.model, self.return_scene, None)
					return
				
	
	def render(self, screen, rc):
		interesting_coords = self.base_interesting_coords
		if self.current_valid_coord != None:
			interesting_coords = interesting_coords + [[self.item_type] + list(self.current_valid_coord)]
		
		ROOM_RENDERER.render(screen, rc, None, None, interesting_coords, None, None, True, None)
		
		text = 'Cancel'
		yoffset = 0
		if self.item_type == None:
			text = 'Done'
			yoffset = -int(abs(math.sin(rc * 2 * 3.14159 / 30) * 5))
		
		TEXT.render(screen, text, 'yellow' if self.is_over_done else 'white', 8, 8 + yoffset)
		
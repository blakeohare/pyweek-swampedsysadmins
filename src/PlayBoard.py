import pygame
import random

from src.Util import *
from src.DragDescriptor import DragDescriptor
from src.ImageLibrary import IMAGES

class Tile:
	def __init__(self, id, flags):
		self.id = id
		passable = False
		for flag in list(flags):
			if flag == 'p':
				passable = True
		self.passable = passable
	
	

_TILE_MANIFEST = """
.	p
x	-
""".strip()

RAW_OFFICE = """
xxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxx
x......x...........x
x......x...........x
x..................x
x..................x
x......x...........x
x......x...........x
xxxxxxxx...........x
@      x...........x
@      x...........x
@      x...........x
@      x...........x
@      x...........x
@      xxxxxxxxxxxxx
""".lower().strip()


TILE_MANIFEST = {}
for row in _TILE_MANIFEST.split('\n'):
	row = row.strip()
	cols = row.split('\t')
	id = cols[0]
	flags = cols[1]
	TILE_MANIFEST[id] = Tile(id, flags)

office_rows = RAW_OFFICE.split('\n')
office_height = len(office_rows)
office_width = len(office_rows[0])

OFFICE = make_grid(office_width, office_height)
y = 0
while y < office_height:
	x = 0
	row = office_rows[y].strip().replace('@', ' ')
	while x < office_width:
		OFFICE[x][y] = TILE_MANIFEST.get(row[x], None)
		x += 1
	y += 1

class PlayBoard:
	def __init__(self, model):
		self.grid = make_grid(10, 10)
		self.selected = None
		self.model = model
		self.drag_descriptor = []
		self.active_drag = None
		self.drag_offset = None
	
	def update(self, events):
		
		if self.active_drag != None and self.active_drag.done:
			self.active_drag = None
		
		for event in events:
			if event.mousedown:
				member = self.find_staff_member(event.x, event.y)
				if member != None:
					self.drag_offset = (member.x - event.x, member.y - event.y)
					drag = DragDescriptor(member)
					drag.is_active = True
					self.drag_descriptor.append(drag)
					member.drag_path = drag
					self.active_drag = drag
			elif event.mouseup:
				if self.active_drag != None:
					self.active_drag.is_active = False
					self.active_drag = None
					
			elif event.mousemove:
				if self.active_drag != None:
					nx = event.x + self.drag_offset[0]
					ny = event.y + self.drag_offset[1]
					
					px, py = self.active_drag.points[-1]
					if self.is_line_segment_okay(px, py, nx, ny):
						self.active_drag.add_point(nx, ny, self)
		
		
		
		self.model.session.update(self)
		
		for member in self.model.staff:
			member.update(self)
	
	def get_random_open_tile(self):
		# this isn't called very often so it can be stupid and brute force
		potential = []
		y = 4
		while y <= 14:
			x = 10
			while x <= 18:
				tile = OFFICE[x][y]
				if tile != None and tile.passable:
					potential.append((x, y))
				x += 1
			y += 1
		random.shuffle(potential)
		return potential[0]
		
	def is_line_segment_okay(self, start_x, start_y, end_x, end_y):
		start_col = int(start_x // 32)
		start_row = int(start_y // 32)
		end_col = int(end_x // 32)
		end_row = int(end_y // 32)
		
		if start_col == end_col and start_row == end_row:
			return self.is_tile_okay(start_col, start_row)
		
		start_and_end_okay = self.is_tile_okay(start_col, start_row) and self.is_tile_okay(end_col, end_row)
		if not start_and_end_okay:
			return False
		
		d = abs(end_row - start_row) + abs(end_col - start_col)
		if d == 1:
			return True
		if d == 2:
			if start_x > end_x:
				start_x, end_x = end_x, start_x
				start_y, end_y = end_y, start_y
				start_col, end_col = end_col, start_col
				start_row, end_row = end_row, start_row
			
			dx = end_x - start_x
			dy = end_y - start_y
			
			if dx == 0: # HOW?!?!?
				return True
			m = dy / dx
			
			if m == 1 or m == -1:
				for x in [start_col, end_col]:
					for y in [start_row, end_row]:
						if not self.is_tile_okay(start_col, start_row):
							return False
				return True
			to_next_x = start_col * 32 - start_x
			y = m * to_next_x + start_y
			row = int(y // 32)
			if row == start_row:
				return self.is_tile_okay(end_col, row)
			else:
				return self.is_tile_okay(start_col, row)
			
			
		mx = (start_x + end_x) // 2
		my = (start_y + end_y) // 2
		
		return self.is_line_segment_okay(start_x, start_y, mx, my) and self.is_line_segment_okay(mx, my, end_x, end_y)
	
	def is_tile_okay(self, col, row):
		if col < 0: return False
		if row < 0: return False
		if col >= office_width: return False
		if row >= office_height: return False
		tile = OFFICE[col][row]
		if tile == None: return False
		return tile.passable
	def find_staff_member(self, x, y):
		for member in self.model.staff:
			left = member.x - 16
			right = member.x + 16
			top = member.y - 64
			bottom = member.y
			if x >= left and x <= right and y >= top and y <= bottom:
				return member
		return None
	
	def render(self, screen, rc, left_offset, top_offset, staff):
		# will have to merge staff and doodads
		
		#self.render_collision_hints(screen, left_offset, top_offset)
		
		bg = IMAGES.get('the_room.png')
		screen.blit(bg, (0, 0))
		
		render_list = []
		for member in staff:
			member.render(rc, render_list)
			if member.drag_path != None:
				for dot in member.drag_path.get_marker_list(rc):
					x, y = dot
					render_list.append(('R', y * 1000000, x - 1, y - 1, 2, 2, (255, 255, 0)))
			
		for device in self.model.session.active_devices:
			device.render(rc, render_list)
			
		render_list.sort(key = lambda x:x[1])
		
		for entity in render_list:
			type = entity[0]
			if type == 'I':
				img = entity[2]
				x = entity[3]
				y = entity[4]
				screen.blit(img, (x + left_offset, y + top_offset))
			elif type == 'R':
				x = entity[2]
				y = entity[3]
				w = entity[4]
				h = entity[5]
				color = entity[6]
				pygame.draw.rect(screen, color, pygame.Rect(x, y, w, h))
		
	
	def render_collision_hints(self, screen, left, top):
		width = len(OFFICE)
		height = len(OFFICE[0])
		
		y = 0
		while y < office_height:
			x = 0
			while x < office_width:
				tile = OFFICE[x][y]
				if tile != None:
					color = (20, 20, 20) if tile.passable else (100, 100, 100)
					pygame.draw.rect(screen, color, pygame.Rect(left + x * 32, top + y * 32, 32, 32))
				x += 1
			y += 1
		
import pygame

from src.Util import *
from src.DragDescriptor import DragDescriptor

class Tile:
	def __init__(self, id, flags):
		self.id = id
		passable = False
		for flag in list(flags):
			if flag == 'p':
				passable = True
		self.passable = passable
	
	

_TILE_MANIFEST = """
-	p
x	-
""".strip()

RAW_OFFICE = """
xxxxxxxxxxxxxxxxxxxx
x......x...........x
x......x...........x
x......x...........x
x......x...........x
x......x...........x
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
		
		for event in events:
			if event.mousedown:
				member = self.find_staff_member(event.x, event.y)
				if member != None:
					drag = DragDescriptor(member, event.x, event.y)
					self.drag_descriptor.append(drag)
					member.drag_path = drag
					self.active_drag = drag
					self.drag_offset = (member.x - event.x, member.y - event.y)
			elif event.mouseup:
				if self.active_drag != None:
					self.active_drag = None
			elif event.mousemove:
				if self.active_drag != None:
					self.active_drag.add_point(event.x + self.drag_offset[0], event.y + self.drag_offset[1], self)
		
		
		
		for member in self.model.staff:
			member.update(self)
	
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
		
		self.render_collision_hints(screen, left_offset, top_offset)
		
		render_list = []
		for member in staff:
			member.render(rc, render_list)
			if member.drag_path != None:
				for dot in member.drag_path.get_marker_list(rc):
					x, y = dot
					render_list.append(('R', y * 1000000, x - 1, y - 1, 2, 2, (0, 255, 0)))
			
			
			
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
		
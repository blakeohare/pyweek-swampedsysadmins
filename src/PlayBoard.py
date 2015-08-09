import pygame

from src.Util import *

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
	def __init__(self):
		self.grid = make_grid(10, 10)
	
	def render(self, screen, rc, left_offset, top_offset, staff):
		# will have to merge staff and doodads
		
		self.render_collision_hints(screen, left_offset, top_offset)
		
		images = []
		for member in staff:
			img = member.render(rc)
			if img != None:
				images.append(img)
		
		images.sort(key = lambda x:x[2] * 100000 + x[1])
		
		for entity in images:
			image, x, y = entity
			screen.blit(image, (x + left_offset, y + top_offset))
		
	
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
		
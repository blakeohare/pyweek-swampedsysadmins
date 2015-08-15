import pygame
import random

from src.Util import *
from src.DragDescriptor import DragDescriptor
from src.ImageLibrary import IMAGES
from src.RoomRenderer import ROOM_RENDERER

class Tile:
	def __init__(self, id, flags):
		self.id = id
		passable = False
		self.denoted = False
		for flag in list(flags):
			if flag == 'p':
				passable = True
			elif flag == 'd':
				self.denoted = True
				
		self.passable = passable
		
	
	

_TILE_MANIFEST = """
.	p
x	-
i	d
j	d
t	d
c	d
""".strip()

RAW_OFFICE = """
xxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxx
xi...c.............x
x..................x
x..................x
x..................x
x..................x
x.t..j.............x
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


INTERESTING_COORDS = {}

# session is nullable
def build_office_map(session, interesting_coords_out, model):

	interesting_coords = []
	output = make_grid(office_width, office_height)
	y = 0
	while y < office_height:
		x = 0
		row = office_rows[y].strip().replace('@', ' ')
		while x < office_width:
			id = row[x]
			tile = TILE_MANIFEST.get(id, None)
			if tile != None and tile.denoted:
				interesting_coords.append((id, x, y))
				tile = TILE_MANIFEST['.']
			output[x][y] = tile
			x += 1
		y += 1
	
	blocking = TILE_MANIFEST['x']
	furniture = []
	for mf in model.furniture:
		interesting_coords.append((mf[0], mf[1], mf[2]))
	
	interesting_coords += furniture
	
	while len(interesting_coords_out) > 0:
		interesting_coords_out.pop(0)
	
	for interesting in interesting_coords:
		interesting_coords_out.append(interesting)
		key, x, y = interesting
		if key == 'i':
			if session == None or session.is_iv_available():
				output[x][y] = blocking
				output[x + 1][y] = blocking
		elif key == 'c':
			if session == None or session.is_cucumber_available():
				output[x][y] = blocking
				output[x + 1][y] = blocking
		elif key == 't':
			if session == None or session.is_tape_available():
				output[x][y] = blocking
				output[x + 1][y] = blocking
		elif key == 'j':
			if session == None or session.is_jacket_available():
				output[x][y] = blocking
				output[x + 1][y] = blocking
		elif key in '12345':
			width, height = {
				'1': (1, 1),
				'2': (2, 1),
				'3': (1, 1),
				'4': (2, 2),
				'5': (3, 2)
			}[key]
			xstart = x
			ystart = y
			xend = x + width
			yend = y + height
			for x in range(xstart, xend):
				for y in range(ystart, yend):
					output[x][y] = blocking
	
	return output
			

class PlayBoard:
	def __init__(self, model):
		self.interesting_coords = []
		self.office = build_office_map(model.session, self.interesting_coords, model)
		self.selected = None
		self.model = model
		self.drag_descriptor = []
		self.active_drag = None
		self.drag_offset = None
		self.level_completed = False
		self.animations = []
		
	
	def update(self, events):
		
		if self.active_drag != None and self.active_drag.done:
			self.active_drag = None
		
		for event in events:
			if event.mousedown:
				members = self.find_staff_members(event.x, event.y) # find staff in range
				if len(members) > 0:
					sorted_members = []
					for member in members:
						dx = member.x - event.x
						dy = member.y - event.y
						dist = dx ** 2 + dy ** 2
						if self.is_line_segment_okay(event.x, event.y, member.x, member.y):
							sorted_members.append((dist, member, False))
						else:
							sorted_members.append((dist, member, True)) # this 3rd item is whether or not the clicked point is okay. If it isn't, then fall back to the old behavior with the offset
					sorted_members.sort(key=lambda x:x[0])
					
					if len(sorted_members) > 0:
						ignore, member, use_offset = sorted_members[0]
						if use_offset:
							self.drag_offset = (member.x - event.x, member.y - event.y)
						else:
							self.drag_offset = (0, 0)
						drag = DragDescriptor(member)
						drag.is_active = True
						self.drag_descriptor.append(drag)
						member.drag_path = drag
						self.active_drag = drag
						if not use_offset:
							self.active_drag.add_point(event.x, event.y, self)
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
		
		self.level_completed = self.model.session.is_done()
	
	def get_hover_buttons(self):
		bins = {}
		for interesting in self.interesting_coords:
			if interesting[0] in 'ictj':
				key, x, y = interesting
				bins[key] = (x, y)
		
		output = []
		for staff in self.model.staff:
			if bins.get('i') != None and (staff.holding == None or staff.holding == 'iv'):
				x, y = bins['i']
				x += 1
				y += 1
				x *= 32
				y *= 32
				dx = staff.x - x
				dy = staff.y - y
				
				if dx ** 2 + dy ** 2 < 48 ** 2:
					if staff.holding == None:
						command = 'iv_take_' + str(staff.id)
						label = 'Take IV'
					else:
						command = 'iv_drop_' + str(staff.id)
						label = 'Put back'
					
					button = {
						'id': command,
						'label': label,
						'x': x,
						'y': y - 50
					}
					output.append(button)
					
			if bins.get('c') != None and (staff.holding == None or staff.holding == 'cucumber'):
				x, y = bins['c']
				x += 1
				y += 1
				x *= 32
				y *= 32
				dx = staff.x - x
				dy = staff.y - y
				if dx ** 2 + dy ** 2 < 48 ** 2:
					if staff.holding == None:
						command = 'cuc_take_' + str(staff.id)
						label = 'Take Cucumbers'
					else:
						command = 'cuc_drop_' + str(staff.id)
						label = 'Put back'
					
					button = {
						'id': command,
						'label': label,
						'x': x,
						'y': y - 50
					}
					output.append(button)
				
			if bins.get('t') != None and (staff.holding == None or staff.holding == 'tape'):
				x, y = bins['t']
				x += 1
				y += 1
				x *= 32
				y *= 32
				dx = staff.x - x
				dy = staff.y - y
				if dx ** 2 + dy ** 2 < 48 ** 2:
					if staff.holding == None:
						command = 'tape_take_' + str(staff.id)
						label = 'Pick Tape'
					else:
						command = 'tape_drop_' + str(staff.id)
						label = 'Put back'
					
					button = {
						'id': command,
						'label': label,
						'x': x,
						'y': y - 50
					}
					output.append(button)
				
			if bins.get('j') != None and (staff.holding == None or staff.holding == 'jacket'):
				x, y = bins['j']
				x += 1
				y += 1
				x *= 32
				y *= 32
				dx = staff.x - x
				dy = staff.y - y
				if dx ** 2 + dy ** 2 < 48 ** 2:
					if staff.holding == None:
						command = 'jacket_take_' + str(staff.id)
						label = 'Take Jacket'
					else:
						command = 'jacket_drop_' + str(staff.id)
						label = 'Put back'
					
					button = {
						'id': command,
						'label': label,
						'x': x,
						'y': y - 50
					}
					output.append(button)
			
			if staff.holding != None:
				for device in self.model.session.active_devices:
					if abs(device.x - staff.x) < 32 and abs(device.y - staff.y) < 32 and device.state == 'ailed':
						t = staff.holding + '-' + device.ailment
						if t in ('iv-sick', 'cucumber-sad', 'tape-angry', 'jacket-crazy'):
							output.append({
								'id': 'device_treat_' + str(device.id) + "_" + str(staff.id),
								'label': "Treat",
								'x': device.x,
								'y': device.y - 50
							})
							
		
		return None if len(output) == 0 else output
	
	def get_random_open_tile(self):
		# this isn't called very often so it can be stupid and brute force
		potential = []
		y = 4
		while y <= 14:
			x = 10
			while x <= 18:
				tile = self.office[x][y]
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
		if d == 2 and end_row != start_row and end_col != start_col:
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
		tile = self.office[col][row]
		if tile == None: return False
		return tile.passable
	
	def find_staff_members(self, x, y):
		output = []
		for member in self.model.staff:
			left = member.x - 16
			right = member.x + 16
			top = member.y - 64
			bottom = member.y
			
			padding = 16
			
			left -= padding
			right += padding
			top -= padding
			bottom += padding
			
			if x >= left and x <= right and y >= top and y <= bottom:
				output.append(member)
		return output
	
	
	def render(self, screen, rc, left_offset, top_offset, staff):
		
		supplies = {
			'i': self.model.inventory_ivs > 0,
			'c': self.model.inventory_cucumbers > 0,
			't': self.model.inventory_tapes > 0,
			'j': self.model.inventory_jackets > 0
		}
		
		ROOM_RENDERER.render(screen, rc, self.model.session.active_devices, staff, self.interesting_coords, supplies, self.animations, False)
		
		
	
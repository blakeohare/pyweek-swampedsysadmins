import pygame

from src.PlayBoard import PlayBoard
from src.Model import Model
from src.FontEngine import TEXT
from src.menus.WrapperMenu import WrapperMenu

class PlayScene:
	def __init__(self, level_id):
		self.next = None
		self.model = Model(level_id)
		self.board = PlayBoard(self.model)
		self.hover_buttons = None
		self.active_button = None
	
	def update(self, events, mouse_coords):
		
		events = self.filter_hover_ui_events(events, mouse_coords)
		self.board.update(events)
		
		if self.model.session.is_done():
			self.next = WrapperMenu(self, self.model)
	
	def render(self, screen, rc):
		screen.fill((0, 0, 0))
		
		self.board.render(screen, rc, 0, 0, self.model.staff)
		iv_count = self.model.inventory_ivs
		
		x = 8
		y = 32 * 10
		TEXT.render(screen, "IV'S: " + str(iv_count), 'blue', x, y)
		
		self.render_hover_ui(screen, rc)
	
	def filter_hover_ui_events(self, events, mouse_xy):
		if self.hover_buttons == None or len(self.hover_buttons) == 0: return events
		filtered_events = []
		
		x, y = mouse_xy
		self.active_button = None
		for button in self.hover_buttons:
			if x > button[0] and x < button[2] and y > button[1] and y < button[3]:
				self.active_button = button[4]
		
		for event in events:
			if event.mousedown:
				x = event.x
				y = event.y
				handled = False
				for button in self.hover_buttons:
					if x >= button[0] and x <= button[2] and y >= button[1] and y <= button[3]:
						self.perform_hover_ui_click(button[4])
						handled = True
				if not handled:
					filtered_events.append(event)
			else:
				filtered_events.append(event)
		return events
	
	def perform_hover_ui_click(self, id):
		if id.startswith('iv_take_'):
			if self.model.inventory_ivs > 0:
				staff_member = self.get_staff_member(id[len('iv_take_'):])
				staff_member.holding = 'iv'
				self.model.inventory_ivs -= 1
				return
		elif id.startswith('device_treat_'):
			parts = id.split('_')
			device = self.get_device(int(parts[2]))
			staff = self.get_staff_member(parts[3])
			if staff != None and device != None:
				staff.holding = None
				device.start_treatment()
	
	def get_device(self, id):
		for device in self.model.session.active_devices:
			if device.id == id:
				return device
		return None
	
	def get_staff_member(self, id):
		for member in self.model.staff:
			if member.id ==  id:
				return member
		return None
	
	def render_hover_ui(self, screen, rc):
		buttons = self.board.get_hover_buttons() # { 'id': ..., 'label': ..., 'key':... 'x', 'y'}
		if buttons != None:
			hb = []
			for button in buttons:
				if button['id'] == self.active_button:
					color = (0, 100, 255)
				else:
					color = (0, 0, 140)
				x = button['x']
				y = button['y']
				label = button['label']
				w = 16 * (1 + len(label))
				h = 32
				pygame.draw.rect(screen, color, pygame.Rect(x, y, w, h))
				# TODO: texturing
				TEXT.render(screen, label, 'white', x + 8, y + 8)
				
				hb.append((x, y, x + w, y + h, button['id']))
			self.hover_buttons = hb
		else:
			self.hover_buttons = None
		
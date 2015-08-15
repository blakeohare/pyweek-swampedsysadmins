import pygame
import math

from src.PlayBoard import PlayBoard
from src.Model import Model
from src.FontEngine import TEXT
from src.menus.WrapperMenu import WrapperMenu
from src.menus.OptionsMenu import OptionsMenu
from src.Reward import Reward

MENU_LINK_SIZE = (16 * 5, 20)

class PlayScene:
	def __init__(self, level_id, model = None):
		self.next = None
		if model == None:
			self.model = Model(level_id)
		else:
			self.model = model
		self.board = PlayBoard(self.model)
		self.hover_buttons = None
		self.active_button = None
		self.mosue_xy = (99999, 999999)
		self.last_shown_budget = self.model.budget
	
	def update(self, events, mouse_coords):
		
		events = self.filter_hover_ui_events(events, mouse_coords)
		self.board.update(events)
		
		if self.model.session.is_done():
			reward = Reward(self.model, self.model.session)
			self.model.budget += reward.calculate_next_budget()
			self.model.reward = reward
			self.next = WrapperMenu(self, self.model)
		
		self.mouse_xy = mouse_coords
	
	def render(self, screen, rc):
		screen.fill((0, 0, 0))
		
		self.board.render(screen, rc, 0, 0, self.model.staff)
		
		budget = self.model.budget
		display_budget = self.last_shown_budget
		if abs(budget - display_budget) < 2:
			display_budget = budget
		else:
			display_budget = (display_budget + budget) // 2
		self.last_shown_budget = display_budget
		
		x = 8
		y = 32 * 10 - 8
		things = [
			("Budget", display_budget, 'white'),
			("IV's", self.model.inventory_ivs, 'blue'),
			("Cucumbers", self.model.inventory_cucumbers, 'green'),
			('Tapes', self.model.inventory_tapes, 'gray'),
			('Jackets', self.model.inventory_jackets, 'purple'),
			('Laptops', self.model.inventory_laptops, 'white'),
			('Phones', self.model.inventory_phones, 'white'),
			('Tablets', self.model.inventory_tablets, 'white')
		]
		
		
		y_offset = int(abs(math.sin(rc * 2 * 3.14159 / 30)) * 3)
		first = True
		for thing in things:
			prefix = ''
			if first:
				prefix = '$'
			
			count = thing[1]
			label = thing[0] + ': ' + prefix + str(count)
			color = thing[2]
			yo = 0
			if count < 2:
				color = 'red'
				if count < 1:
					yo = -y_offset
			TEXT.render(screen, label, color, x, y + yo)
			y += 18
			if first:
				first = False
				y += 15
		
		self.render_hover_ui(screen, rc)
	
	def filter_hover_ui_events(self, events, mouse_xy):
		hb = self.hover_buttons
		if self.hover_buttons == None: hb = []
		filtered_events = []
		
		x, y = mouse_xy
		self.active_button = None
		for button in hb:
			if x > button[0] and x < button[2] and y > button[1] and y < button[3]:
				self.active_button = button[4]
		
		
		
		for event in events:
			if event.mousedown:
				x = event.x
				y = event.y
				handled = False
				
				if x < 16 * 5 and y < 20:
					self.click_menu()
					handled = True
				else:
					for button in hb:
						if x >= button[0] and x <= button[2] and y >= button[1] and y <= button[3]:
							self.perform_hover_ui_click(button[4])
							handled = True
							break
							
				if not handled:
					filtered_events.append(event)
			else:
				filtered_events.append(event)
		return events
	
	def click_menu(self):
		
		self.next = OptionsMenu(self)
	
	def perform_hover_ui_click(self, id):
		if id.startswith('iv_take_'):
			if self.model.inventory_ivs > 0:
				staff_member = self.get_staff_member(id[len('iv_take_'):])
				staff_member.holding = 'iv'
				self.model.inventory_ivs -= 1
				return
		elif id.startswith('cuc_take_'):
			if self.model.inventory_cucumbers > 0:
				staff_member = self.get_staff_member(id[len('cuc_take_'):])
				staff_member.holding = 'cucumber'
				self.model.inventory_cucumbers -= 1
				return
		elif id.startswith('tape_take_'):
			if self.model.inventory_tapes > 0:
				staff_member = self.get_staff_member(id[len('tape_take_'):])
				staff_member.holding = 'tape'
				self.model.inventory_tapes -= 1
				return
		elif id.startswith('jacket_take_'):
			if self.model.inventory_jackets > 0:
				staff_member = self.get_staff_member(id[len('jacket_take_'):])
				staff_member.holding = 'jacket'
				self.model.inventory_jackets -= 1
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
		id = int(id)
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
		
		color = 'white'
		if self.mouse_xy[0] < MENU_LINK_SIZE[0] and self.mouse_xy[1] < MENU_LINK_SIZE[1]:
			color = 'yellow'
		TEXT.render(screen, 'Menu', color, 8, 4)
		
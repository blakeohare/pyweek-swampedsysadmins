import pygame
import math

from src.PlayBoard import PlayBoard
from src.Model import Model
from src.FontEngine import TEXT
from src.menus.WrapperMenu import WrapperMenu
from src.menus.OptionsMenu import OptionsMenu
from src.menus.YouLose import YouLose
from src.Reward import Reward
from src.Sound import SND

from src.menus.TextHover import TextHover

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
		self.mouse_xy = (99999, 999999)
		self.last_shown_budget = self.model.budget
		self.first = True
		self.enable_tutorial = level_id == 0
		self.tut_last = -1
		self.tut_count = 0
		
		if self.enable_tutorial:
			self.model.budget = 10000
			self.model.inventory_ivs = 5
			self.model.inventory_cucumbers = 0
			self.model.inventory_jackets = 0
			self.model.inventory_tapes = 0
			
	
	def do_tutorial_update(self):
		self.tut_count += 1
		
		if self.tut_last == -1:
			self.next = TextHover([
				'\n'.join([
					'Welcome #5779 to the IT department at',
					'Zephyr, Pencil, & Bear International.',
					'Your job is to fix malfunctioning',
					'devices our employees bring to you.'])], self)
			self.tut_last = 0
			
			self.model.session.induce_device('laptop', 'sick')
		elif self.tut_last == 0:
			if self.tut_count > 80:
				
				self.next = TextHover([
					'\n'.join([
						'This is a laptop.']),
					'\n'.join([
						'This floating face above it means the',
						'laptop is sick. We make sick devices',
						'well again with an IV.']),
					'\n'.join([
						'Go get one from the medical supply ',
						'bin in the corner.'])], self)
				self.tut_last = 1
		elif self.tut_last == 1:
			if self.model.staff[0].holding == 'iv':
				self.next = TextHover([
					'\n'.join([
						'Now go back to the sick laptop and',
						'treat it.'])], self)
				self.tut_last = 2
				self.tut_count = 0
		
		elif self.tut_last == 2:
			device = self.model.session.active_devices[0]
			if device.state_counter > 5 * 30:
				device.state_counter = 300
			if device.state == 'treated':
				self.next = TextHover([
					'\n'.join([
						'Each treatment has a progress bar.',
						'If the life bar above it runs out ',
						'before the treatment finishes, the ',
						'device dies. Do not let that happen.'])], self)
				self.tut_last = 3
				self.model.session.induce_device('laptop', 'sad')
				self.model.inventory_cucumbers = 2
				self.tut_count = 0
		elif self.tut_last == 3:
			if self.tut_count > 80:
				self.next = TextHover([
					'\n'.join([
						'This laptop is not sick, but it is ',
						'sad. It needs a spa treatment to ',
						'cheer up. Go get a cucumber from the',
						'table to the right of the IV bin.'])], self)
				self.tut_last = 4
				self.tut_count = 0
		elif self.tut_last == 4:
			device = self.model.session.active_devices[-1]
			if device.state_counter > 10 * 30:
				device.state_counter = 300
			if device.state == 'treated':
				self.next = TextHover([
					'\n'.join([
						'Notice that the spa treatment is ',
						'slower than the IV. Each type of ',
						'treatment takes a different length of',
						'time, so plan accordingly.'])], self)
				self.tut_last = 5
				self.tut_count = 0
				self.model.session.induce_device('tablet', 'angry')
		elif self.tut_last == 5:
			if self.tut_count > 80:
				self.next = TextHover([
					'\n'.join([
						'This is a tablet.  Here at Zephyr,',
						'Pencil, & Bear International, we ',
						'fully embrace all computing ',
						'paradigms, be they touch, voice, or',
						'good old keyboard and mouse.']),

					'\n'.join([
						'This tablet is angry.  It needs a ',
						'whale songs audio tape to calm down.',
						'Go get one from the tape shelf.']),
						
					'\n'.join([
						'We eagerly await the arrival of scent',
						'based computing, so we can announce ',
						'that we are the first in our industry',
						'to adopt what will undoubtedly be a ',
						'revolution in computing.'])], self)
				self.model.inventory_tapes = 2
				self.tut_last = 6
				self.tut_count = 0
		elif self.tut_last == 6:
			device = self.model.session.active_devices[-1]
			if device.state_counter > 10 * 30:
				device.state_counter = 300
			if device.state == 'treated':
				self.next = TextHover([
					'\n'.join([
						'Tapes take longer than IVs and',
						'spa treatments.'])], self)
				self.tut_last = 7
				self.tut_count = 0
				self.model.inventory_jackets = 2
				self.model.session.induce_device('phone', 'crazy')
		elif self.tut_last == 7:
			if self.tut_count > 80:
				
				self.next = TextHover([
					'\n'.join([
						'This is a phone.  It has gone crazy.',
						'It needs a straitjacket to contain it',
						'until it reboots.  Go get a jacket',
						'from the coat rack.'])], self)
				self.tut_last = 8
				self.tut_count = 0
			
		elif self.tut_last == 8:
			device = self.model.session.active_devices[-1]
			if device.state_counter > 10 * 30:
				device.state_counter = 300
			if device.state == 'treated':
				self.next = TextHover([
					'\n'.join([
						'Jackets are the slowest treatment.',
						'That concludes the four treatment',
						'types.'])], self)
				self.tut_last = 9
				self.tut_count = 0
		elif self.tut_last == 9:
			if len(self.model.session.active_devices) == 0:
				self.next = TextHover([
					'\n'.join([
						'But wait! There is more!'])], self)
				self.tut_last = 10
				self.tut_count = 0
				self.model.session.induce_device('phone', 'unknown')
		elif self.tut_last == 10:
			if self.tut_count > 80:
				
				self.next = TextHover([
					'\n'.join([
						'Some devices do not say what is wrong',
						'with them.  Go stand on the phone to',
						'diagnose it with your shoes.'])], self)
				self.tut_last = 11
				self.tut_count = 0
		elif self.tut_last == 11:
			device = self.model.session.active_devices[-1]
			if device.state_counter > 10 * 30:
				device.state_counter = 300
			if device.ailment != 'unknown':
				self.next = TextHover([
					'\n'.join([
						'Now that the phone has been',
						'diagnosed, it can be treated.',
						'Go do so.'])], self)
				self.tut_last = 12
				self.tut_count = 0
		elif self.tut_last == 12:
			device = self.model.session.active_devices[-1]
			if device.state_counter > 10 * 30:
				device.state_counter = 300
			if device.ailment == 'treated':
				self.tut_last = 13
				self.tut_count = 0
				self.model.session.induce_device_storm()
		elif self.tut_last == 13:
			if len(self.model.session.active_devices) < 5:
				self.next = TextHover([
					'\n'.join([
						'If a device goes too long without ',
						'being treated, or its treatment does',
						'not finish in time, it dies.']),

					'\n'.join([
						'Any device that dies must be ',
						'replaced.  If a spare is available, ',
						'it will be removed from inventory.']),
						
					'\n'.join([
						'If no spares are available, a ',
						'replacement will be rush ordered, ',
						'with the cost deducted from the ',
						'budget. This is expensive.']),
						
					'\n'.join([
						'If the budget goes negative, you and',
						'your department will be ',
						'incinera^H^H^H^H^H^H^Hfired.']),
						
					'\n'.join([
						'After each round, a performance ',
						'review, and possibly a budget ',
						'allowance, will be given.']),
						
					'\n'.join([
						'The budget may be used for ',
						'- restocking inventory',
						'- productivity enhances',
						'- hiring coworkers',
						'',
						'It also pays your salary']),
						
					'\n'.join([
						'This concludes the new ',
						'employee training program.'])], self)
				self.tut_last = 14
				self.tut_count = 0
		elif self.tut_last == 14:
			if self.tut_count > 120:
				from src.menus.TitleScene import TitleScene
				self.next = TitleScene()
				
			
	
	def update(self, events, mouse_coords):
		
		if self.first:
			self.first = False
			if self.enable_tutorial:
				SND.music_tutorial()
			else:
				SND.music_game()
		
		if self.enable_tutorial:
			self.do_tutorial_update()
		
		if self.model.budget < 0:
			self.next = YouLose(self)
		
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
		
		level = self.model.session.level
		if level == 0:
			header = 'New Employee Training'
		else:
			header = 'Day ' + str(level)
		TEXT.render(screen, header, 'white', 300, 4)
	
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
		if '_drop_' in id:
			if id.startswith('iv_drop_'):
				self.model.inventory_ivs += 1
				staff_member = self.get_staff_member(id[len('iv_drop_'):])
				staff_member.holding = None
				return
			elif id.startswith('cuc_drop_'):
				self.model.inventory_cucumbers += 1
				staff_member = self.get_staff_member(id[len('cuc_drop_'):])
				staff_member.holding = None
				return
			elif id.startswith('tape_drop_'):
				self.model.inventory_tapes += 1
				staff_member = self.get_staff_member(id[len('tape_drop_'):])
				staff_member.holding = None
				return
			elif id.startswith('jacket_drop_'):
				self.model.inventory_jackets += 1
				staff_member = self.get_staff_member(id[len('jacket_drop_'):])
				staff_member.holding = None
				return
		
		elif id.startswith('iv_take_'):
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
		
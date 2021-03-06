import math
import random

from src.ImageLibrary import IMAGES

from src.Sound import SND

FLYING_FRAMES = 30
START_X = 400
START_Y = 30

ID_ALLOC = [1]

SICK_TREAT_TIME = 30 * 6
SAD_TREAT_TIME = 30 * 7
ANGRY_TREAT_TIME = 30 * 8
CRAZY_TREAT_TIME = 30 * 9
UNKNOWN_TREAT_TIME = 30 * 6

STARTING_TTL = 30 * 40

AILMENTS = 'sick sad angry crazy'.split(' ')

class Device:
	def __init__(self, playboard, game_time, device_type, x, y, ailment):
		self.id = ID_ALLOC[0]
		ID_ALLOC[0] += 1
		self.start = game_time
		self.end = None
		self.response_time = 0
		self.type = 'device'
		self.device_type = device_type # { 'phone', 'tablet', 'laptop' }
		self.x = START_X
		self.y = START_Y
		self.landing_x, self.landing_y = playboard.get_random_open_tile()
		self.landing_x = self.landing_x * 32 + 16
		self.landing_y = self.landing_y * 32 + 16
		self.ttl = STARTING_TTL
		
		self.ailment = ailment # { 'sick', 'sad', 'angry', 'crazy', 'dead', 'unknown' }
		self.actual_ailment = random.choice(AILMENTS)
		self.unknown_discovery_counter = 0
		self.state = 'flying' # { 'flying', 'ailed', 'treated', 'new', 'dead' }
		self.resolution = None
		self.state_counter = 0
		self.playboard = playboard
		self.model = playboard.model
		self.replaced = False
		self.treatment_ratio = 1.0
	
	def start_treatment(self):
		self.state = 'treated'
		self.state_counter = 0
		ratio = 1.0
		for furn in self.playboard.model.furniture:
			if furn[0] == '4':
				ratio *= 1.03
			elif furn[0] == '1':
				dx = self.x - (furn[1] + .5) * 32
				dy = self.y - (furn[2] + .5) * 32
				dist = (dx ** 2 + dy ** 2) ** .5
				if dist <= 32 * 3:
					ratio *= 1.02
			elif furn[0] == '3':
				#print furn, self.x, self.y
				dx = self.x - (furn[1] + .5) * 32
				dy = self.y - (furn[2] + .5) * 32
				dist = (dx ** 2 + dy ** 2) ** .5
				#print 'distance', dist
				if dist <= 32 * 3:
					ratio *= 1.10
				
		#print ratio
		self.treatment_ratio = ratio
	
	def update(self):
		self.state_counter += 1
		self.ttl -= 1
		if self.state == 'flying':
			self.ttl = STARTING_TTL # still immune to the aging process while flying through the air
			progress = 1.0 * self.state_counter / FLYING_FRAMES
			antiprogress = 1 - progress
			self.x = int(START_X * antiprogress + self.landing_x * progress)
			self.y = int(START_Y * antiprogress + self.landing_y * progress)
			if self.state_counter == FLYING_FRAMES:
				self.x = self.landing_x
				self.y = self.landing_y
				self.state = 'ailed'
				self.state_counter = 0
				if self.ailment == 'dead':
					self.state = 'dead'
		elif self.state == 'dead':
			if not self.replaced:
				self.replaced = True
				t = self.device_type
				self.resolution = 'ordered'
				if t == 'phone':
					if self.model.inventory_phones > 0:
						self.resolution = 'replaced'
						self.model.inventory_phones -= 1
					else:
						self.model.special_order_phone()
				elif t == 'tablet':
					if self.model.inventory_tablets > 0:
						self.resolution = 'replaced'
						self.model.inventory_tablets -= 1
					else:
						self.model.special_order_tablet()
				elif t == 'laptop':
					if self.model.inventory_laptops > 0:
						self.resolution = 'replaced'
						self.model.inventory_laptops -= 1
					else:
						self.model.special_order_laptop()
					
		elif self.state == 'ailed':
			self.response_time += 1
			if self.ailment == 'unknown':
				for staff in self.playboard.model.staff:
					dx = staff.x - self.x
					dy = staff.y - self.y
					if dx ** 2 + dy ** 2 < 32 ** 2:
						self.unknown_discovery_counter += 1
			
				if self.unknown_discovery_counter >= UNKNOWN_TREAT_TIME:
					self.ailment = self.actual_ailment
		elif self.state == 'treated':
			self.response_time += 1
			if self.ailment == 'sick':
				treat_time = SICK_TREAT_TIME
			elif self.ailment == 'sad':
				treat_time = SAD_TREAT_TIME
			elif self.ailment == 'angry':
				treat_time = ANGRY_TREAT_TIME
			elif self.ailment == 'crazy':
				treat_time = CRAZY_TREAT_TIME
			elif self.ailment == 'dead':
				treat_time = 9999999 # won't happen
			elif self.ailment == 'unknown':
				treat_time = UNKNOWN_TREAT_TIME
			
			if self.state_counter * self.treatment_ratio >= treat_time:
				self.state = 'new'
				self.resolution = 'treated'
				self.state_counter = 0
				SND.play_device_fix()
		
		if self.ttl < 0 and self.state != 'dead':
			self.state = 'dead'
			self.state_counter = 0
	
	
	def render(self, rc, render_list):
		sort_key = self.y * 1000000
		
		progress_bar = None
		
		if self.state == 'flying':
			mid = FLYING_FRAMES // 2
			zeroToOne = 1.0 - ((self.state_counter - mid) ** 2.0) / (mid ** 2.0)
			py_offset = int(zeroToOne * 80)
			self.draw_image(render_list, IMAGES.get('devices/' + self.device_type + '.png'), sort_key, self.x, self.y - py_offset)
		elif self.state == 'ailed':
			self.draw_image(render_list, IMAGES.get('devices/' + self.device_type + '.png'), sort_key, self.x, self.y)
			ailment = IMAGES.get('devices/' + self.ailment + '.png')
			py_offset = int(math.sin(3.14159 + self.state_counter * 2 * 3.14159 / 150) * 10 + 30)
			self.draw_image(render_list, ailment, sort_key + 1, self.x, self.y - py_offset)
			
			if self.ailment == 'unknown' and self.unknown_discovery_counter > 0:
				progress_bar = [
					(0, 128, 255),
					self.unknown_discovery_counter,
					UNKNOWN_TREAT_TIME
				]
		elif self.state == 'treated':
			if self.ailment == 'sick':
				treatment_time = SICK_TREAT_TIME
				self.draw_image(render_list, IMAGES.get('devices/' + self.device_type + '.png'), sort_key, self.x, self.y)
				self.draw_image(render_list, IMAGES.get('treatments/iv_rack.png'), sort_key - 1, self.x - 16, self.y,)
			elif self.ailment == 'sad':
				treatment_time = SAD_TREAT_TIME
				self.draw_image(render_list, IMAGES.get('devices/' + self.device_type + '_cucumber.png'), sort_key, self.x, self.y)
			elif self.ailment == 'angry':
				treatment_time = ANGRY_TREAT_TIME
				self.draw_image(render_list, IMAGES.get('devices/' + self.device_type + '_headphones.png'), sort_key, self.x, self.y)
			elif self.ailment == 'crazy':
				treatment_time = CRAZY_TREAT_TIME
				self.draw_image(render_list, IMAGES.get('devices/' + self.device_type + '_straightjacket.png'), sort_key, self.x, self.y)
			else:
				raise Exception("No rendering code for ailment treatment.")
			
			counter = int(self.treatment_ratio * self.state_counter)
			if counter > treatment_time: counter = treatment_time
			
			progress_bar = [
				(0, 255, 0),
				self.state_counter,
				treatment_time
			]
		else:
			self.draw_image(render_list, IMAGES.get('devices/' + self.device_type + '.png'), sort_key, self.x, self.y)

		if progress_bar != None:
			numerator = progress_bar[1]
			treatment_time = progress_bar[2]
			color = progress_bar[0]
			progress = 1.0 * numerator / treatment_time
			if progress > 1.0:
				progress = 1.0
			
			width = 50
			height = 8
			x = self.x - 12
			y = self.y + 8
			self.draw_rectangle(render_list, sort_key, x, y, width, height, (100, 100, 100))
			self.draw_rectangle(render_list, sort_key, x, y, int(width * progress), height, color)
		
		if self.state == 'ailed' or self.state == 'treated':
			progress = 1.0 * self.ttl / STARTING_TTL
			color = (0, 180, 0)
			if progress > .5:
				if progress > .75:
					color = (0, 100, 200)
				else:
					color = (0, 180, 0)
			elif progress > .25:
				color = (255, 255, 0)
			elif progress > .1:
				color = (255, 128, 0)
			else:
				color = (255, 0, 40)
			
			
			width = 50
			height = 8
			x = self.x - 12
			y = self.y
			self.draw_rectangle(render_list, sort_key, x, y, width, height, (100, 100, 100))
			self.draw_rectangle(render_list, sort_key, x, y, int(width * progress), height, color)
		
	def draw_image(self, rl, img, sort, x, y):
		rl.append(('I', sort, img, x - img.get_width() // 2, y - img.get_height()))

	def draw_rectangle(self, rl, sort, x, y, width, height, color):
		rl.append(('R', sort, x, y, width, height, color))
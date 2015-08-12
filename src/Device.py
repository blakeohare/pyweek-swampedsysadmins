import math

from src.ImageLibrary import IMAGES

FLYING_FRAMES = 30
START_X = 400
START_Y = 30

ID_ALLOC = [1]

SICK_TREAT_TIME = 30 * 6

class Device:
	def __init__(self, playboard, game_time, device_type, x, y, ailment):
		self.id = ID_ALLOC[0]
		ID_ALLOC[0] += 1
		self.start = game_time
		self.end = None
		self.type = 'device'
		self.device_type = device_type # { 'phone', 'tablet', 'laptop' }
		self.x = START_X
		self.y = START_Y
		self.landing_x, self.landing_y = playboard.get_random_open_tile()
		self.landing_x = self.landing_x * 32 + 16
		self.landing_y = self.landing_y * 32 + 16
		
		self.ailment = ailment # { 'sick', 'sad', 'angry', 'crazy', 'dead', 'unknown' }
		self.state = 'flying' # { 'flying', 'ailed', 'treated', 'new', 'dead' }
		self.resolution = None
		self.state_counter = 0
	
	def start_treatment(self):
		self.state = 'treated'
		self.state_counter = 0
	
	def update(self):
		self.state_counter += 1
		if self.state == 'flying':
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
					self.resolve_dead_device()
		elif self.state == 'dead':
			self.resolution = 'replaced' # TODO: this needs to be dependent on whether you have enough reserves
		elif self.state == 'ailed':
			pass
		elif self.state == 'treated':
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
			
			if self.state_counter >= treat_time:
				self.state = 'new'
				self.resolution = 'treated'
				self.state_counter = 0
	
	def resolve_dead_device(self):
		model = self.playboard.model
		if self.type == 'laptop':
			if model.inventory_laptops > 0:
				self.resolution = 'replaced'
				model.inventory_laptops -= 1
			else:
				self.resolution = 'ordered'
		elif self.type == 'phone':
			if model.inventory_phones > 0:
				self.resolution = 'replaced'
				model.inventory_phones -= 1
			else:
				self.resolution = 'ordered'
		elif self.type == 'tablet':
			if model.inventory_tablets > 0:
				self.resolution = 'replaced'
				model.inventory_tablets -= 1
			else:
				self.resolution = 'ordered'
		
	
	def render(self, rc, render_list):
		sort_key = self.y * 1000000
		
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
		elif self.state == 'treated':
			if self.ailment == 'sick':
				self.draw_image(render_list, IMAGES.get('devices/' + self.device_type + '.png'), sort_key, self.x, self.y)
				self.draw_image(render_list, IMAGES.get('treatments/iv_rack.png'), sort_key - 1, self.x - 16, self.y,)
				treatment_time = 30 * 6
				progress = 1.0 * self.state_counter / treatment_time
				if progress > 1.0:
					progress = 1.0
			else:
				raise Exception("No rendering code for ailment treatment.")
			
			width = 50
			height = 8
			x = self.x - 12
			y = self.y + 8
			self.draw_rectangle(render_list, sort_key, x, y, width, height, (100, 100, 100))
			self.draw_rectangle(render_list, sort_key, x, y, int(width * progress), height, (0, 255, 0))
		else:
			self.draw_image(render_list, IMAGES.get('devices/' + self.device_type + '.png'), sort_key, self.x, self.y)
		
	def draw_image(self, rl, img, sort, x, y):
		rl.append(('I', sort, img, x - img.get_width() // 2, y - img.get_height()))

	def draw_rectangle(self, rl, sort, x, y, width, height, color):
		rl.append(('R', sort, x, y, width, height, color))
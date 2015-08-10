import math

from src.ImageLibrary import IMAGES

FLYING_FRAMES = 30
START_X = 400
START_Y = 30

class Device:
	def __init__(self, playboard, game_time, device_type, x, y, ailment):
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
		elif self.state == 'dead':
			pass
		elif self.state == 'ailed':
			pass
		elif self.state == 'treated':
			pass
	
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
		else:
			self.draw_image(render_list, IMAGES.get('devices/' + self.device_type + '.png'), sort_key, self.x, self.y)
		
	def draw_image(self, rl, img, sort, x, y):
		rl.append(('I', sort, img, x - img.get_width() // 2, y - img.get_height()))

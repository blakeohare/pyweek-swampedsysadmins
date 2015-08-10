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
		elif self.state == 'ailing':
			pass
		elif self.state == 'treated':
			pass
	
	def render(self, rc, render_list):
		img = None
		if self.state == 'flying':
			img = IMAGES.get('devices/' + self.device_type + '.png')
		elif self.state == 'ailing':
			img = IMAGES.get('devices/' + self.device_type + '.png')
		
		# TODO: all this
		img = IMAGES.get('devices/' + self.device_type + '.png')
		
		py_offset = 0
		if self.state == 'flying':
			mid = FLYING_FRAMES // 2
			zeroToOne = 1.0 - ((self.state_counter - mid) ** 2.0) / (mid ** 2.0)
			py_offset = int(zeroToOne * 80)
		render_list.append(('I', self.y * 1000000, img, self.x - img.get_width() // 2, self.y - img.get_height() - py_offset))
	

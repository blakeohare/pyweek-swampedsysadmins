import pygame
import math

from src.ImageLibrary import IMAGES

VELOCITY = 1.5

class Staff:
	def __init__(self, id):
		# as a person
		self.id = id
		self.happiness = .5
		
		# as a sprite
		self.x = 64
		self.y = 96
		self.direction = 's'
		self.moving = False
		self.target_x = 0
		self.target_y = 0
		self.move_please = False
		self.drag_path = None
		
		self.holding = None
		
		self.velocity = 5.0
		
		self.TODO_remove_me = pygame.Surface((32, 64)).convert()
		self.TODO_remove_me.fill((0, 255, 255))
		self.playboard = None
		
		self.images = None # dictionary. keys are 'walk_n0' through 'walk_n3' and 'stand_n'
		
	
	def convert_vector_to_dir(self, x, y):
		ang = math.atan2(y, x)
		piOver4 = 3.14159265358979 / 4
		if ang < -3 * piOver4 or ang > 3 * piOver4: return 'w'
		if ang < piOver4 and ang > -piOver4: return 'e'
		if y < 0: return 'n'
		return 's'
			
	
	def update(self, playboard):
		self.playboard = playboard
		self.moving = False
		
		if self.drag_path != None:
			old_x, old_y = self.x, self.y
			self.drag_path.do_update(self.velocity)
			new_x, new_y = self.x, self.y
			dx = new_x - old_x
			dy = new_y - old_y
			if dx != 0 or dy != 0:
				self.moving = True
				self.direction = self.convert_vector_to_dir(dx, dy)
			
			if self.drag_path.done:
				self.drag_path = None
		
		'''
		if self.move_please:
			dx = self.target_x - self.x
			dy = self.target_y - self.y
			
			dist = (dx ** 2 + dy ** 2) ** .5
			
			if dist < VELOCITY:
				self.x = self.target_x
				self.y = self.target_y
				self.move_please = False
				self.moving = False
			else:
				dx = VELOCITY * dx / dist
				dy = VELOCITY * dy / dist
				self.moving = True'''
	
	def get_current_image(self, rc):
		images = self.images
		if images == None:
			images = {}
			composite = IMAGES.get('staff/composite.png')
			y = self.id * 64
			x = 0
			for dir in 'nsew':
				for action in ['stand', 'walk']:
					suffixes = [''] if (action == 'stand') else ('0', '1', '2', '3')
					for suffix in suffixes:
						img = pygame.Surface((32, 64)).convert()
						img.fill((255, 0, 255))
						img.blit(composite, (-x, -y))
						img.set_colorkey((255, 0, 255))
						key = action + '_' + dir + suffix
						images[key] = img
						x += 32
			self.images = images
			
		if self.moving:
			return images['walk_' + self.direction + str((rc // 3) & 3)]
		return images['stand_' + self.direction]
		
	def render(self, rc, render_list):
		img = self.get_current_image(rc)
		width, height = img.get_size()
		
		
		px = int(self.x) - width // 2
		py = int(self.y) - height
		
		# Image: I, sort value, image, x, y
		render_list.append(('I', self.y * 1000000 + self.x, img, px, py))
		
		#if self.playboard != None and self.playboard.selected == self:
		#	# Rectangle: R, sort value, 
		#	render_list.append(('R', self.y * 1000000 + self.x - 1, px - 2, py - 2, img.get_width() + 4, img.get_height() + 4, (255, 255, 255)))
	
		if self.holding != None:
			if self.holding == 'iv':
				img = IMAGES.get('treatments/iv_bag.png')
			elif self.holding == 'cucumber':
				img = IMAGES.get('treatments/cucumber.png')
			elif self.holding == 'tape':
				img = IMAGES.get('treatments/tape.png')
			elif self.holding == 'jacket':
				img = IMAGES.get('treatments/jacket.png')
			else:
				raise Exception("Invalid item holding." + self.holding)
				
			render_list.append(('I', self.y * 1000000 + self.x + 1, img, self.x - img.get_width() // 2, self.y - 64 - img.get_height()))
				
	
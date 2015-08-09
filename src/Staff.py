import pygame
import math

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
		
		self.velocity = 2.6
		
		self.TODO_remove_me = pygame.Surface((32, 64)).convert()
		self.TODO_remove_me.fill((0, 255, 255))
		self.playboard = None
		
	
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
		
	def render(self, rc, render_list):
		img = self.TODO_remove_me # TODO images when Christine checks them in
		
		width, height = img.get_size()
		
		
		px = int(self.x) - width // 2
		py = int(self.y) - height
		
		# Image: I, sort value, image, x, y
		render_list.append(('I', self.y * 1000000 + self.x, img, px, py))
		
		if self.playboard != None and self.playboard.selected == self:
			# Rectangle: R, sort value, 
			render_list.append(('R', self.y * 1000000 + self.x - 1, px - 2, py - 2, img.get_width() + 4, img.get_height() + 4, (255, 255, 255)))
	
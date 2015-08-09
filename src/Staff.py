import pygame

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
		
		self.TODO_remove_me = pygame.Surface((32, 64)).convert()
		self.TODO_remove_me.fill((0, 255, 255))
		self.playboard = None
		
		
	def update(self, playboard):
		self.playboard = playboard
		self.moving = False
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
				self.moving = True
		
	def set_target(self, x, y):
		self.move_please = True
		self.target_x = x
		self.target_y = y
		
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
	
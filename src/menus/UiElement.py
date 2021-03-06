import pygame

from src.FontEngine import TEXT

class UiElement:
	def __init__(self, type):
		self.type = type # { BUTTON, TEXT, IMAGE }
	
	def render(self, screen, offset_x, offset_y, mouse_xy, rc):
		if self.type == 'TEXT':
			TEXT.render(screen, self.text, self.color, offset_x + self.x, offset_y + self.y)
		elif self.type == 'BUTTON':
			mx, my = mouse_xy
			mx -= offset_x
			hover = False
			is_enabled = self.is_enabled()
			if is_enabled:
				hover = mx >= self.left and mx < self.right
				if hover:
					my -= offset_y
					hover = my >= self.top and my < self.bottom
			
			bg_color = (200, 200, 200, 200) if hover else (40, 40, 40, 200)
			pygame.draw.rect(screen, bg_color, pygame.Rect(offset_x + self.x, offset_y + self.y, self.width, self.height))
			
			color = 'white' if is_enabled else 'gray'
			TEXT.render(screen, self.text, color, offset_x + self.text_x, offset_y + self.text_y)
		elif self.type == 'IMAGE':
			if self.frames == 1:
				img = self.image[0]
			else:
				frame = (rc // 4) % self.frames
				img = self.image[frame]
			screen.blit(img, (self.x + offset_x, self.y + offset_y))
		
		elif self.type == 'HOVER':
			mx, my = mouse_xy
			mx -= offset_x
			my -= offset_y
			if mx >= self.left  and mx < self.right and my >= self.top and my < self.bottom:
				self.element.text = self.text
		else:
			raise Exception("Not implemented.")


def create_ui_button(text, function, x, y, width, height, is_enabled_lambda):
	text = str(text)
	button = UiElement('BUTTON')
	button.action = function
	button.x = x
	button.y = y
	button.width = width
	button.height = height
	button.is_enabled = is_enabled_lambda
	button.left = x
	button.top = y
	button.right = x + width
	button.bottom = y + height
	button.text = text
	button.text_x = button.x + (width - len(text) * 16) // 2
	button.text_y = button.y + (height - 16) // 2
	return button

def create_ui_text(text, color, x, y):
	text = str(text)
	output = UiElement('TEXT')
	output.text = text
	output.color = color
	output.x = x
	output.y = y
	output.width = len(text) * 16
	output.height = 16
	return output

def create_ui_image_list(images, x, y):
	output = create_ui_image(images[0], x, y)
	output.image = images[:]
	output.frames = len(images)
	return output

def create_ui_image(img, x, y):
	output = UiElement('IMAGE')
	output.image = [img]
	output.frames = 1
	output.x = x
	output.y = y
	output.left = x
	output.top = y
	output.width = img.get_width()
	output.height = img.get_height()
	output.right = x + output.width
	output.bottom = y + output.height
	return output

def create_ui_hover_region(text_element, left, top, right, bottom, text):
	output = UiElement('HOVER')
	output.element = text_element
	output.left = left
	output.top = top
	output.bottom = bottom
	output.right = right
	output.text = text
	return output
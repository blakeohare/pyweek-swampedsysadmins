from src.Util import *
from src.FontEngine import TEXT

class YouLose:
	def __init__(self, bg):
		self.bg = bg
		self.next = None
		self.counter = 0
		self.allow_click = False
	
	def update(self, events, mxy):
		self.counter += 1
		for event in events:
			if event.mouseup and self.allow_click:
				from src.menus.TitleScene import TitleScene
				self.next = TitleScene()
				
	def render(self, screen, rc):
		self.bg.render(screen, rc)
		
		alpha = int(self.counter * 5)
		if alpha > 180:
			alpha = 180
		
		draw_alpha_rectangle(screen, 0, 0, screen.get_width(), screen.get_height(), 100, 0, 0, alpha)
		
		if alpha == 180:
			self.allow_click = True
			message = [
				'Due to the lack of responsiveness',
				'to the incoming repair requests,',
				'the IT department has singlehandedly',
				'bankrupted ZP&B Inc, creating',
				'a snowball effect that has sent the',
				'global economy into a crash only',
				'describable as a second dark age.',
				'',
				'tap anywhere to submit resume to',
				'your local feudal lord.'
			]
			
			y = 20
			x = 20
			for line in message:
				TEXT.render(screen, line, 'white', x, y)
				y += 32
			
			
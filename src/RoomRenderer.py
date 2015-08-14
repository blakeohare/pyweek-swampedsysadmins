import pygame

from src.ImageLibrary import IMAGES

class RoomRenderer:

	def __init__(self):
		pass
		
	def render(self, screen, rc, nullable_devices, nullable_staff, interesting_coords, nullable_supplies, mutable_animations):
		
		render_list = []
		
		bg = IMAGES.get('the_room.png')
		render_list.append(('I', -1, bg, 0, 0))
		
		if nullable_staff != None:
			for member in nullable_staff:
				member.render(rc, render_list)
				if member.drag_path != None:
					for dot in member.drag_path.get_marker_list(rc):
						x, y = dot
						render_list.append(('R', y * 1000000, x - 1, y - 1, 2, 2, (255, 255, 0)))
		
		if nullable_devices != None:
			for device in nullable_devices:
				device.render(rc, render_list)
			
		for key in interesting_coords.keys():
			x, y = interesting_coords[key]
			
			has_any = nullable_supplies == None or nullable_supplies.get(key, True) # default to true for placement screen
			if key == 'i':
				file = 'ivs'
			elif key == 'c':
				file = 'cucumber_station'
				x += .3
			elif key == 't':
				file = 'tape_shelf'
			elif key == 'j':
				file = 'jacket_rack'
			
			path = 'treatments/' + file + '_' + ('full' if has_any else 'empty') + '.png'
			img = IMAGES.get(path)
			render_list.append(('I', (y + 1) * 32 * 1000000, img, int(x * 32), (y + 1) * 32 - img.get_height()))
		
		i = 0
		while i < len(mutable_animations):
			animation = mutable_animations[i]
			images = []
			if animation['type'] == 'device':
				images.append(IMAGES.get('devices/' + animation['device'] + '.png'))
				images.append(IMAGES.get('devices/' + animation['overlay'] + '.png'))
			ttl = animation['ttl']
			ttl -= 1
			animation['ttl'] = ttl
			
			for img in images:
				render_list.append(('I', animation['mx'] + animation['my'] * 1000000, img, animation['x'] - img.get_width() // 2, animation['y'] - img.get_height()))
				
			animation['x'] += animation['vx']
			animation['y'] += animation['vy']
			
			if ttl > 0:
				i += 1
			else:
				mutable_animations.pop(i)

		self.draw_to_screen(screen, render_list)

	def draw_to_screen(self, screen, items):

		items.sort(key = lambda x:x[1])
		
		for item in items:
			type = item[0]
			if type == 'I':
				type, sort, img, x, y = item
				
				screen.blit(img, (x, y))
				
			elif type == 'R':
				type, sort, x, y, w, h, color = item
				pygame.draw.rect(screen, color, pygame.Rect(x, y, w, h))

ROOM_RENDERER = RoomRenderer()
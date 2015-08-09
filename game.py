import pygame
import time

from src.constants import *
from src.menus.TitleScene import TitleScene
from src.Event import Event
from src.MagicPotato import MAGIC_POTATO

def main():

	pygame.init()
	is_fullscreen = False
	resizeable = 0 #pygame.RESIZABLE
	
	real_screen = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption("Some Sysadmins")
	virtual_screen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), resizeable)
	active_scene = TitleScene()
	
	mouse_pos = (0, 0)
	counter = 0
	while True:
		
		begin = time.time()
		
		if MAGIC_POTATO.is_full_screen() != is_fullscreen:
			is_fullscreen = MAGIC_POTATO.is_full_screen()
			if is_fullscreen:
				real_screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
			else:
				real_screen = pygame.display.set_mode(SCREEN_SIZE, resizeable)
				
		events = []
		last_mouse_event = None
		for e in pygame.event.get():
			if e.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = e.pos
				x, y = mouse_pos
				last_mouse_event = Event('mousedown', x, y, e.button == 1)
				events.append(last_mouse_event)
				
			elif e.type == pygame.MOUSEBUTTONUP:
				mouse_pos = e.pos
				x, y = mouse_pos
				last_mouse_event = Event('mouseup', x, y, e.button == 1)
				events.append(last_mouse_event)
			elif e.type == pygame.MOUSEMOTION:
				mouse_pos = e.pos
				x, y = mouse_pos
				last_mouse_event = Event('mousemove', x, y, False)
				events.append(last_mouse_event)
			elif e.type == pygame.QUIT:
				return
			elif e.type == pygame.KEYDOWN:
				pressed_keys = pygame.key.get_pressed()
				
				if e.key == pygame.K_F4 and (pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]):
					return
				elif e.key == pygame.K_w and (pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]):
					return
				elif e.key == pygame.K_ESCAPE:
					return
			elif e.type == pygame.VIDEORESIZE:
				w, h = e.size
				SCREEN_SIZE[0] = w
				SCREEN_SIZE[1] = h
				real_screen = pygame.display.set_mode(SCREEN_SIZE, resizeable)
		if last_mouse_event != None:
			mouse_pos = (last_mouse_event.x, last_mouse_event.y)
		
		active_scene.update(events, mouse_pos)
		active_scene.render(virtual_screen, counter)
		
		pygame.transform.scale(virtual_screen, real_screen.get_size(), real_screen)
		
		pygame.display.flip()
		
		next_scene = active_scene.next
		if next_scene != None:
			active_scene.next = None
			active_scene = next_scene
		
		if active_scene == None:
			return
		
		counter += 1
		
		end = time.time()
		
		diff = end - begin
		delay = 1.0 / FPS
		wait = delay - diff
		if wait > 0:
			time.sleep(wait)

main()

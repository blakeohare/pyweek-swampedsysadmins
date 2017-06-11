MUSIC_GAMEPLAY = 'RingOfSpinningElephants, TheTransistorProletariat'

MUSIC_MENU = '1LOfMilk'

MUSIC_TUTORIAL = '1LOfMilk'

MUSIC_TITLE = 'BabyBlueWallpaper'

CUCUMBER_TAKE = 'knife'
IV_TAKE = None
JACKET_TAKE = None
TAPE_TAKE = 'tape0, tape1'

DEVICE_FIX = 'ding' #', '.join(map(lambda x:('marimba-' + ('0' if (x < 10) else '') + str(x) + '.wav'), range(1, 17)))
DEVICE_DEAD = None



import pygame
import os
import random

from src.MagicPotato import MAGIC_POTATO

class SoundPlayer:
	def __init__(self):
		self.sounds = {}
		self.current_song = None
		#self.volume = MAGIC_POTATO.get_music_volume()
	
	def ensure_music_volume(self):
		potato_volume = MAGIC_POTATO.get_music_volume() / 100.0
		mixer_volume = pygame.mixer.music.get_volume()
		if abs(potato_volume - mixer_volume) > .001:
			pygame.mixer.music.set_volume(potato_volume)
	
	def _play_music(self, id):
		if id != None:
			pygame.mixer.music.set_volume(MAGIC_POTATO.get_music_volume())
			if self.current_song != id:
				self.current_song = id
				songs = []
				for t in id.split(','):
					songs.append(t.strip())
				song = random.choice(songs)
				pygame.mixer.music.load('music' + os.sep + song + '.ogg')
				pygame.mixer.music.play(-1)
	
	def _play_sound(self, id):
		if id != None:
			snd = self.sounds.get(id, None)
			if snd == None:
				snd = []
				for t in id.split(','):
					t = t.strip()
					file = id
					if not file.endswith('.wav'):
						file += '.ogg'
					snd.append(pygame.mixer.Sound('sfx' + os.sep + file))
				self.sounds[id] = snd
			
			sound = None
			if len(snd) == 1:
				sound = snd[0]
			elif len(snd) > 1:
				sound = random.choice(snd)
			
			if sound != None:
				sound.set_volume(MAGIC_POTATO.get_sound_volume())
				sound.play()
	
	def play_cucumber_take(self): self._play_sound(CUCUMBER_TAKE)
	def play_iv_take(self): self._play_sound(IV_TAKE)
	def play_jacket_take(self): self._play_sound(JACKET_TAKE)
	def play_tape_take(self): self._play_sound(TAPE_TAKE)
	def play_device_fix(self): self._play_sound(DEVICE_FIX)
	def play_device_dead(self): self._play_sound(DEVICE_DEAD)
		

	def music_game(self):
		self._play_music(MUSIC_GAMEPLAY)
	
	def music_menu(self):
		self._play_music(MUSIC_MENU)

	def music_tutorial(self):
		self._play_music(MUSIC_TUTORIAL)

	def music_title(self):
		self._play_music(MUSIC_TITLE)
		


SND = SoundPlayer()
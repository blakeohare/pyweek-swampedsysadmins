class MagicPotato:
	def __init__(self):
		self._sound_volume = .7
		self._music_volume = .7
		self._is_full_screen = False
	
	def get_sound_volume(self):
		return int(self._sound_volume * 100)
	
	def set_sound_volume(self, percent):
		if percent < 0: percent = 0
		if percent > 100: percent = 100
		ratio = percent / 100.0
		self._sound_volume = ratio
	
	def get_music_volume(self):
		return int(self._music_volume * 100)
	
	def set_music_volume(self, percent):
		if percent < 0: percent = 0
		if percent > 100: percent = 100
		ratio = percent / 100.0
		self._music_volume = ratio
	
	def is_full_screen(self):
		return self._is_full_screen
	
	def set_full_screen(self, value):
		self._is_full_screen = value
	
MAGIC_POTATO = MagicPotato()

import pygame
from random import randint

class Text():
	def __init__(self, x, y, text, size, **kwargs):
		self.x = x
		self.y = y
		self.text = text
		self.size = size
		# changes
		self.color = (randint(0,255), randint(0,255), randint(0,255))
		self.duration = -1			# last forever
		self.change = False			# not change color
		self.xytopleft = False		# start in the middle of text box
		self.xybottomright = False	# start in the middle of text box
		self.font_name = "comic sans ms"
		self.typing = False
		# kwargs
		for kwarg in kwargs.items():
			if kwarg[0] == 'duration':		# change the duration of temporaries
				self.duration = kwarg[1]
			elif kwarg[0] == 'color':		# change the start color
				self.color = kwarg[1]
			elif kwarg[0] == 'change':		# bool for changing the color over time
				self.change = kwarg[1]
			elif kwarg[0] == 'topleft':		# bool for start xy as top left
				self.xytopleft = kwarg[1]
			elif kwarg[0] == 'bottomright':	# bool for start xy as bottom right
				self.xybottomright = kwarg[1]
			elif kwarg[0] == 'font':		# change font
				self.font_name = kwarg[1]
			elif kwarg[0] == 'typing':		# type each letter
				self.typing = kwarg[1]
				self.original_text = text				# original text
				self.text = ""
				self.max_time_typing = 30
				self.time_typing = 0
		# generate textbox
		self.create_texbox()

	def create_texbox(self):
		self.font = pygame.font.SysFont(self.font_name, self.size)
		self.textbox = self.font.render(self.text, True, self.color)
		self.width = self.textbox.get_width()
		self.height = self.textbox.get_height()

	def duration_ended(self):
		return self.duration == 0

	def new_color(self):
		self.color = (randint(50,255), randint(50,255), randint(50,255))

	def change_text(self, new_text):
		self.text = new_text
		self.create_texbox()

	def update(self):
		# change  color
		if self.change:
			r = 3	# range of change rgb
			new_c = list(self.color)
			i = randint(0,2)	# chooses between r,g,b
			new_c[i] = (new_c[i] + randint(-r,r)) % 255
			self.color = (new_c[0], new_c[1], new_c[2])
		# type a letter
		if self.typing:
			if self.time_typing == 0:
				self.time_typing += self.max_time_typing
				# add a letter
				qtd = len(self.text) +1		# n letters used until now
				self.change_text(self.original_text[qtd:])
				# end of text
				if qtd >= len(self.original_text):
					self.duration = 0
					self.typing = False
			else:
				self.time_typing -= 1
		# decrease duration
		if self.duration > 0:
			self.duration -= 1

	def render(self, window):
		if self.xytopleft:			# x,y top left
			x = self.x
			y = self.y
		elif self.xybottomright:	# x,y bottom right
			x = self.x - self.width
			y = self.y - self.height
		else:						# x,y center
			x = self.x - self.width//2
			y = self.y - self.height//2
		window.blit(self.textbox, (x,y))

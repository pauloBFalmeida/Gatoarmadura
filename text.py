import pygame
from random import randint

class Text():
	def __init__(self, x, y, text, size):
		self.x = x
		self.y = y
		self.text = text
		self.size = size
		self.color = (randint(0,255), randint(0,255), randint(0,255))

	def new_color(self):
		self.color = (randint(0,255), randint(0,255), randint(0,255))

	def update(self):
		r = 3	# range
		new_c = list(self.color)
		i = randint(0,2)
		new_c[i] = (new_c[i] + randint(-r,r)) % 255
		self.color = (new_c[0], new_c[1], new_c[2])

	def render(self, window):
		font = pygame.font.SysFont("comic sans ms", self.size)
		textbox = font.render(self.text, True, self.color)
		x = self.x - textbox.get_width()//2
		y = self.y - textbox.get_height()//2
		window.blit(textbox, (x,y))

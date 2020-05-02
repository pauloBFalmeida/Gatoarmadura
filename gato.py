import pygame
from random import randint
from manipulador_imagem import Manipulador

class Gato():
	def __init__(self, x, y):
		# corpo / armadura
		self.x = x
		self.y = y

		# cabeca do gato
		self.head = Manipulador((100, 100),"gato")
		self.head_x_plus = 0
		self.head_direction = 1

		# armadura
		self.armor = Manipulador((200, 150),"armadura")

	def accelerate(self, x_speed, y_speed):
		# vertex x
		if abs(self.x_speed) < self.max_x_speed:
			self.x_speed += x_speed * self.acceleration
		# vertex y
		if abs(self.y_speed) < self.max_y_speed:
			self.y_speed += y_speed * self.acceleration

	def head_animation(self):
		dist = 10
		velocidade = 0.5
		if (abs(self.head_x_plus) > dist):
			self.head_direction *= -1
		self.head_x_plus += velocidade * self.head_direction

	def update(self):
		self.head_animation()

	def movement_update(self, x_speed, y_speed):
		x_speed *= 2
		y_speed *= 2
		# update position
		self.x += x_speed
		self.y += y_speed

	def render(self, window):
		self.render_armor(window, self.y-40)
		self.render_head(window, self.y)
		size = int(12)
		x = self.x - size//2
		y = self.y - size//2
		# debug, red dot in the midle
		# pygame.draw.rect(window, (255,0,0), (x, y, size, size))
		# pygame.draw.rect(window, (0,255,0), (self.head_x-2, self.y-10-2, 4, 4))

	def render_armor(self, window, y):
		x = self.x - self.armor.size[0]/2
		# y = y - self.armor.size[1]
		window.blit(self.armor.image, (x,y))

	def render_head(self, window, y):
		x = (self.x + self.head_x_plus) - self.head.size[0]/2
		y = y - self.head.size[1]
		window.blit(self.head.image, (x,y))

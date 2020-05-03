import pygame
from random import randint
from manipulador_imagem import Manipulador

class Gato():
	def __init__(self, x, y):
		# position
		self.x = x
		self.y = y
		self.move = False
		# cabeca do gato
		self.head = Manipulador((100, 100),"gato")
		self.head_x_plus = 0
		self.head_direction = 1
		self.head_dist = randint(7,12)
		self.head_speed = float(randint(3,7))/10
		# armadura
		self.armor = Manipulador((200, 150),"armadura")
		self.conjunto_armaduras = [
			Manipulador((200, 150),"armadura") for _ in range(5)
		]
		# attack
		self.attack_ready = False

	def is_attack_ready(self):
		return self.attack_ready

	def set_attack_ready(self):
		self.attack_ready = True

	def attack(self, enemy):
		pass

	def  destruir_armadura(self):
		try:
			self.conjunto_armaduras.pop()
		except:
			print("sem armaduras")

# update
	def update(self):
		self.head_animation()

	def movement_update(self, x_speed, y_speed):
		if self.move:
			x_speed *= 2
			y_speed *= 2
			# update position
			self.x += x_speed
			self.y += y_speed

	def head_animation(self):
		if (abs(self.head_x_plus) > self.head_dist):
			self.head_direction *= -1
		self.head_x_plus += self.head_speed * self.head_direction

# render
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
		try:
			armor = self.conjunto_armaduras[-1]
			x = self.x - armor.size[0]/2
			# y = y - self.armor.size[1]
			window.blit(armor.image, (x,y))
		except:
			print("sem armaduras pra render")
		# x = self.x - self.armor.size[0]/2
		# # y = y - self.armor.size[1]
		# window.blit(self.armor.image, (x,y))

	def render_head(self, window, y):
		x = (self.x + self.head_x_plus) - self.head.size[0]/2
		y = y - self.head.size[1]
		window.blit(self.head.image, (x,y))

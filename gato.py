import pygame
from random import randint
from text import Text
from parte import Parte
from math import sin, cos, radians

class Gato():
	def __init__(self, x, y, right_direction):
		self.vivo = True
		# position
		self.x = x
		self.y = y
		self.move = False
		# armadura
		# self.armor = Manipulador((200, 150),"armadura") # pra pegar pos dos outros
		self.qtd_armaduras = 3
		self.conjunto_armaduras = [Parte((200, 150),"armadura")	for _ in range(self.qtd_armaduras)]
		self.ultima_armadura = None
		armor = self.conjunto_armaduras[-1]
		# cabeca
		self.head_x_plus = 0
		self.head_direction = 1
		self.head_dist = randint(7,12)
		self.head_speed = float(randint(3,7))/10
		self.head = Parte((100, 100),"gato")
		# perna
		self.perna = Parte((150, 150),"perna",fundo=self.head.get_cor_fundo())
		# perna
		self.braco = Parte((100, 150),"braco",fundo=self.head.get_cor_fundo())
		self.right_direction = right_direction
		# attack
		self.attack_ready = False
		self.attacking = False
		self.add_rotation = -1
		self.max_rotation = 40
		self.down_animation = True
		# teste
		self.hit=[-5,-5]
		# print(cos(radians(45)))

	def prepare_battle(self):
		self.move = False
		self.attack_ready = False

	def start_battle(self,enemy):
		self.enemy = enemy
		self.attack_ready = True
		self.move = True

	def is_attack_ready(self):
		return self.attack_ready

	def attack(self):
		self.attacking = True
		self.attack_ready = False
		self.move = False

	def end_attack(self):
		self.attacking = False
		self.attack_ready = True
		self.move = True

	def get_knife_var(self):
		rad = abs(radians(self.braco.rotation))
		var_x = sin(rad) * self.braco.eixo_y
		var_y = sin(rad) * self.braco.eixo_x

		var_x *= 1.5
		var_y *= 2

		return (var_x, var_y)

	def get_knife_pos(self):
		armor = self.conjunto_armaduras[-1]
		y = self.y + armor.top
		if not self.right_direction:	# indo pra esquerda
			x = self.x + armor.left - 10
		else:
			x = self.x + armor.right + 15

		# get variation with angle
		var_x, var_y = self.get_knife_var()

		add_x = self.braco.eixo_x + var_x
		if not self.right_direction: add_x *= -1

		x += add_x
		y += -self.braco.eixo_y + var_y

		return (x, y)

	def inside_hitbox(self, knife_x, knife_y):
		enemy = self.enemy
		armor = enemy.conjunto_armaduras[-1]
		if (knife_x > enemy.x + armor.left) and (knife_x < enemy.x + armor.right):
			# y start in top of screen
			if (knife_y < enemy.y + armor.bot) and (knife_y > enemy.y + armor.top):
				return True
		return False

	def in_range(self):
		knife_x, knife_y = self.get_knife_pos()
		return self.inside_hitbox(knife_x, knife_y)

	def  destruir_armadura(self):
		self.qtd_armaduras -= 1
		self.ultima_armadura = self.conjunto_armaduras.pop()
		if self.qtd_armaduras == 0:
			self.vivo = False
		# play sound
		r = randint(1,5)
		arquivo = "sons/meow"+str(r)+".mp3"
		pygame.mixer.music.load(arquivo)
		pygame.mixer.music.play(0)

	def coletar_armadura(self):
		self.conjunto_armaduras.append(self.enemy.ultima_armadura)
		self.qtd_armaduras += 1

# update
	def update(self):
		if self.vivo:
			self.head_animation()
			if self.attacking:
				self.rotation_update()

	def rotation_update(self):
		# rotacao pra esq ou dir
		add_rotation = self.add_rotation if self.right_direction else -self.add_rotation
		# fim descer animacao
		if self.down_animation and abs(self.braco.rotation) >= self.max_rotation:
			self.down_animation = False
			if self.in_range():
				self.enemy.destruir_armadura()
		# fim subir animacao
		elif not self.down_animation and self.braco.rotation == 0:
			self.down_animation = True
			self.end_attack()
		# descer animacao
		elif self.down_animation:
			self.braco.rotate(add_rotation)
		# subir animacao
		elif not self.down_animation:
			self.braco.rotate(-add_rotation)

	def movement_update(self, x_speed, y_speed):
		if self.move:
			x_speed *= 2
			y_speed *= 2
			# update position
			self.x += x_speed
			self.y += y_speed
			# update right_direction
			if not self.attacking:
				if x_speed > 0: # indo pra direita
					self.right_direction = True
				if x_speed < 0: # indo pra esquerda
					self.right_direction = False

	def head_animation(self):
		if (abs(self.head_x_plus) > self.head_dist):
			self.head_direction *= -1
		self.head_x_plus += self.head_speed * self.head_direction

# render
	def render(self, window):
		if self.vivo:
			self.render_perna(window)
			self.render_braco(window)
			self.render_armor(window)
			self.render_head(window)

	def render_perna(self, window):
		x = self.x
		y = self.y + self.conjunto_armaduras[-1].bot + 45
		self.perna.render(window, x, y)

	def render_braco(self, window):
		# flip image if necessarie
		self.braco.lado(self.right_direction)
		armor = self.conjunto_armaduras[-1]
		if not self.right_direction:	# indo pra esquerda
			x = self.x + armor.left - 10
		else:
			x = self.x + armor.right + 15

		# ajust
		y = self.y + armor.top
		var_x = 0
		if not self.right_direction:
			var_x = -self.get_knife_var()[0]
		self.braco.render(window, x+var_x, y)

		# old
		# pygame.draw.rect(window, (0,255,0), (x,y,self.braco.size[0],self.braco.size[1]))
		# window.blit(image, (x,y))
		self.hit[0] = x
		self.hit[1] = y
		pygame.draw.rect(window, (0,255,0), (self.hit[0],self.hit[1],5,5))

		x,y = self.get_knife_pos()
		pygame.draw.rect(window, (255,0,0), (x,y,2,2))

	def render_armor(self, window):
		armor = self.conjunto_armaduras[-1]
		x = self.x + armor.left
		y = self.y + armor.top
		pygame.draw.rect(window, (0,255,0), (x,y, armor.size[0], armor.size[1]))
		try:
			self.conjunto_armaduras[-1].render(window, self.x, self.y)
		except: pass

	def render_head(self, window):
		x = self.x + self.head_x_plus
		y = self.y + self.conjunto_armaduras[-1].top - 5
		self.head.render(window, x, y)

import pygame
from random import randint
from text import Text
from manipulador_imagem import Manipulador

class Gato():
	def __init__(self, x, y, right_direction):
		self.vivo = True
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
		self.armor = Manipulador((200, 150),"armadura") # pra pegar pos dos outros
		self.conjunto_armaduras = [Manipulador((200, 150),"armadura") for _ in range(3)]
		self.ultima_armadura = None
		self.qtd_armaduras = 3
		# perna
		self.perna = Manipulador((150, 150),"perna",fundo=self.head.get_cor_fundo())
		# perna
		self.braco = Manipulador((100, 150),"braco",fundo=self.head.get_cor_fundo())
		self.right_direction = right_direction
		# attack
		self.attack_ready = False
		self.attacking = False
		self.rotation = 0
		self.add_rotation = -1
		self.min_rotation = -40
		self.down_animation = True

	def start_battle(self,enemy):
		self.enemy = enemy
		self.attack_ready = True
		self.move = True

	def is_attack_ready(self):
		return self.attack_ready

	def attack(self):
		self.attacking = True
		self.attack_ready = False

	def alcance(self):
		margem_x = 30
		margem_y = 20
		min_dist_x = 170
		min_dist_y = 40
		# distancia
		dist_x = self.enemy.x - self.x
		dist_y = self.enemy.y - self.y
		if abs(dist_x) > min_dist_x + margem_x or abs(dist_x) > min_dist_x - margem_x:
			if abs(dist_y) > min_dist_y + margem_y or abs(dist_y) > min_dist_y - margem_y:
				return True
		return False

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
				if self.down_animation and (self.rotation == self.min_rotation or self.rotation == -self.min_rotation):	# fim descer animacao
					self.down_animation = False
					if self.alcance():
						self.enemy.destruir_armadura()
				elif not self.down_animation and self.rotation == 0:			# fim subir animacao
					self.down_animation = True
					self.attacking = False
					self.attack_ready = True
				elif self.down_animation:										# descer animacao
					self.rotation += self.add_rotation if self.right_direction else -self.add_rotation
				elif not self.down_animation:									# subir animacao
					self.rotation -= self.add_rotation if self.right_direction else -self.add_rotation

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
		x = self.x - self.perna.size[0]//2
		y = self.y + self.armor.size[1] - 10
		window.blit(self.perna.image, (x,y))

	def render_braco(self, window):
		image = self.braco.image
		x_modificador = self.armor.size[0]//2 - 30
		if not self.right_direction:	# indo pra esquerda
			image = pygame.transform.flip(image, True, False) #(Surface, xbool, ybool)
			x = self.x - (x_modificador + 100)
		else: 						# canto esquerdo da tela
			x = self.x + x_modificador
		y = self.y -  self.armor.size[1]//2
		if self.rotation != 0:		# rotate
			image = pygame.transform.rotate(image, self.rotation)
		window.blit(image, (x,y))

	def render_armor(self, window):
		try:
			armor = self.conjunto_armaduras[-1]
			x = self.x - armor.size[0]//2
			y = self.y
			window.blit(armor.image, (x,y))
		except: pass

	def render_head(self, window):
		x = (self.x + self.head_x_plus) - self.head.size[0]//2
		y = self.y + 15 - self.armor.size[1]//2
		window.blit(self.head.image, (x,y))

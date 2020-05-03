import pygame
from gato import Gato

class Enemy(Gato):
	def __init__(self, x, y, right_direction):
		Gato.__init__(self,x,y,right_direction)
		self.min_dist_x = 170
		self.min_dist_y = 40

	# def  destruir_armadura(self):
	# 	Gato.destruir_armadura(self)
	# 	speed_x, speed_y = self.aproximar()
	# 	speed_x *= -1
	# 	speed_y *= -1
	# 	for _ in range(15):
	# 		Gato.movement_update(self, speed_x, speed_y)
	# 		Gato.update(self)

	def dist(self):
		# distancia x,y
		return (self.enemy.x - self.x, self.enemy.y - self.y)

	def aproximar(self):
		dist_x, dist_y = self.dist()
		# calcular direcao como -1,0,1
		speed_x = 0
		if abs(dist_x) > self.min_dist_x:
			speed_x = 1 if dist_x > 0 else -1
		speed_y = 0
		if abs(dist_y) > self.min_dist_y:
			speed_y = 1 if dist_y > 0 else -1
		return (speed_x, speed_y)

# render
	def update(self):
		try:
			dist_x, dist_y = self.dist()
			speed_x, speed_y = self.aproximar()
			# se aproximar
			Gato.movement_update(self, speed_x,speed_y)
			# perto o suficiente
			# print()
			if abs(dist_x) <= self.min_dist_x and abs(dist_y) <= self.min_dist_y:
				# pronto para atacar
				if self.attack_ready:
					dist_x, dist_y = self.dist()
					# olhar pro lado certo
					if dist_x > 0 and not self.right_direction:	# enimigo a direita
						Gato.movement_update(self, 1,0)
					elif dist_x < 0 and self.right_direction:	# enimigo a esquerda
						Gato.movement_update(self,-1,0)
					Gato.attack(self)
		except: pass
		Gato.update(self)

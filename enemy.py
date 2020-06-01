import pygame
from gato import Gato

class Enemy(Gato):
	def __init__(self, x, y, right_direction):
		Gato.__init__(self,x,y,right_direction)
		self.min_dist_x = 170
		self.min_dist_y = 40
		# variacao ao atacar
		self.var_knife_x = 72
		self.var_knife_y = 65

	def get_knife_pos_attack(self):
		knife_x, knife_y = self.get_knife_pos()
		# add var to knife pos
		var_x = self.var_knife_x
		if not self.right_direction: var_x *= -1
		knife_x += var_x
		knife_y += self.var_knife_y
		# return
		return(knife_x, knife_y)

	def aproximar(self):
		mov_left = False
		mov_right = False
		mov_top = False
		mov_bot = False
		mov_x = 0
		mov_y = 0
		#
		mg = 5 # margem de erro
		knife_x, knife_y = self.get_knife_pos_attack()
		enemy = self.enemy
		armor = enemy.conjunto_armaduras[-1]
		# #
		# if   knife_x < enemy.x + armor.left: mov_x = 1
		# elif knife_x > enemy.x + armor.right: mov_x = -1
		# elif knife_y < enemy.y + armor.top: mov_y = 1
		# elif knife_y > enemy.y + armor.bot: mov_y = -1

		if knife_x-mg < enemy.x+armor.left:
			mov_right = True
		if knife_x+mg > enemy.x+armor.right:
			mov_left = True

		if knife_y-mg < enemy.y+armor.top:
			mov_bot = True
		if knife_y+mg > enemy.y+armor.bot:
			mov_top = True

		if mov_right and mov_left: mov_x = 0
		elif mov_right: mov_x = 1
		elif mov_left: mov_x = -1

		if mov_top and mov_bot: mov_y = 0
		elif mov_top: mov_y = -1
		elif mov_bot: mov_y = 1

		print()
		if mov_left:print('left')
		if mov_right:print('right')
		if mov_top:print('top')
		if mov_bot:print('bot')

		return (mov_x, mov_y)

	def dentro_alcance(self):
		knife_x, knife_y = self.get_knife_pos_attack()
		# calcular
		return self.inside_hitbox(knife_x, knife_y)

# render
	def update(self):
		try:
			# perto o suficiente para atacar
			# if self.dentro_alcance() and self.attack_ready:
			# 	print('atacar')
			# 	# descubro o lado
			# 	if dist_x > 0 and not self.right_direction:	# enimigo a direita
			# 		Gato.movement_update(self, 1,0)
			# 	elif dist_x < 0 and self.right_direction:	# enimigo a esquerda
			# 		Gato.movement_update(self,-1,0)
			# 	# atacar
			# 	Gato.attack(self)
			# else:

			speed_x, speed_y = self.aproximar()
			# se aproximar
			Gato.movement_update(self, speed_x,speed_y)
			if self.dentro_alcance():
				Gato.attack(self)
		except: pass
		# update
		Gato.update(self)

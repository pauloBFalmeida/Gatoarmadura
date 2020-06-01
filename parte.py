import pygame
from manipulador_imagem import Manipulador

class Parte(Manipulador):
	def __init__(self, size, arquivo, **kwargs):
		# image
		Manipulador.__init__(self, size, arquivo, **kwargs)
		# position
		self.top   = -size[1]//2	# top
		self.bot   = size[1]//2		# bottom
		self.left  = -size[0]//2	# left
		self.right = size[0]//2		# right
		#
		self.right_direction = True
		#
		self.original_image = self.image
		self.rotation = 0
		# point
		self.point_x = 0
		self.point_y = 0
		self.eixo_x = self.image.get_width()//2
		self.eixo_y = self.image.get_height()//2
		# self.angle = self.image.get_width() / self.image.get_height()
		# size_x = (self.braco.size[0]//2)
		# size_y = (self.braco.size[1]//2)
		# hipot = (size_x**2 + size_y**2)**(1/2)

	def lado(self, right_direction):
		# lado foi trocado
		if right_direction != self.right_direction:
			self.right_direction = right_direction
			# flip horizontal
			self.original_image = pygame.transform.flip(self.original_image, True, False)
			# set image as original_image (flipped)
			self.rotate(0)

	def rotate(self, add_rotation):
		self.rotation += add_rotation
		self.image = pygame.transform.rotate(self.original_image, self.rotation)
		# update points
		# self.point_x = self.image.get_width()//2
		# self.point_x *= 1 if self.right_direction else -1
		# self.point_y = self.image.get_height()//2

	def render(self, window, x, y):
		x -= self.size[0]//2
		y -= self.size[1]//2
		# render
		window.blit(self.image, (x, y))

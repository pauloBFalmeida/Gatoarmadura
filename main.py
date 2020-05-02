import pygame
from random import randint
from gato import Gato
from text import Text

pygame.init()

class Gatinhos:
	def __init__(self, width, height, title):
		self.width = width
		self.height = height
		self.win = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)
		icon = pygame.image.load("imagens/gato.png")
		pygame.display.set_icon(icon)
		self.credits = Text(width-65,height-10, "Made by Paulo BF Almeida", 9)

		self.clock = pygame.time.Clock()
		self.running = True
		self.FPS = 60
		self.background = (100, 120, 100)

	def add_sec(self):
		self.sec += 1
		pygame.time.set_timer(pygame.NUMEVENTS-1, 1000)		# wait 1 sec

	def start(self):
		self.gato = Gato(200,200)
		self.gatos = []
		# for i in range(6):
		# 	self.gatos.append(Gato(i*120, i*100))

	def input(self, keys):
		# Player Controls
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			self.gato.movement_update(-1,0)
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			self.gato.movement_update(1,0)
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			self.gato.movement_update(0,-1)
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			self.gato.movement_update(0,1)
		if keys[pygame.K_ESCAPE]:
			self.game_running = False

	def logic(self):
		self.gato.update()
		self.credits.update()
		for g in self.gatos:
			g.update()

	def render(self, window):
		window.fill(self.background)		# background
		self.gato.render(window)
		self.credits.render(window)
		for g in self.gatos:
			g.render(window)
		pygame.display.update()				# update screen

def main():
	game = Gatinhos(800, 600, "Gatinhos")
	game.start()					# start game
	# game.running = False
	while game.running:
		game.clock.tick(game.FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game.running = False
			elif event.type == pygame.NUMEVENTS-1:
				game.add_sec()

		game.input(pygame.key.get_pressed())
		game.logic()
		game.render(game.win)


if __name__ == "__main__":
	main()
	pygame.quit()
	quit()

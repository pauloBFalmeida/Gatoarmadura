# coding: utf-8
import pygame
from random import randint
from time import sleep
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
		self.credits = Text(width-10,
							height-10,
							"Made by Paulo BF Almeida",
							11,
							change=True,
							bottomright=True)

		self.clock = pygame.time.Clock()
		self.running = True
		self.FPS = 60
		self.background = (100, 120, 100)
		# frases
		self.frases = []
		with open('frases.txt') as file:
			 for line in file:
				 self.frases.append(line)

	def add_sec(self):
		self.sec += 1
		pygame.time.set_timer(pygame.NUMEVENTS-1, 1000)		# wait 1 sec

	def prepare_battle(self):
		# create enemy
		self.enemy = Gato(self.width-self.gato.x, self.height-self.gato.y)
		# disable movement
		self.gato.move = False
		self.enemy.move = False
		# say the lines
		self.say_line()
		# start fight
		self.start_battle()

	def say_line(self):
		qtd = (len(self.frases)//2) -1				# qtd de frases
		i = randint(0, qtd) *2						# escolho uma aleatoria
		select = [self.frases[i], self.frases[i+1]]	# pego a pergunta, e a resp
		x_list = [self.gato.x, self.enemy.x]
		y_list = [self.gato.y, self.enemy.y]
		# imprimir na tela
		for j in range(2):
			# posicao
			x = x_list[j]
			y = y_list[j] - 90
			# escrita do lado da cabeca personagem (mais longe do canto)
			x += -130 if x > self.width//2 else 130
			# textbox
			# escrever letra por letra
			# textos = select[j].split()
			# for texto in textos:
			# 	y += 10
			# 	print(texto)
			# 	self.temporarios.append(Text(x,
			# 								y,
			# 								texto,
			# 								20,
			# 								typing=True,
			# 								duration=10))
			self.temporarios.append(Text(x,
											y,
											select[j],	# texto
											20,
											typing=True,
											duration=100*2))

	def start_battle(self):
		self.gato.move = True
		self.enemy.move = True

	def start(self):
		self.tempo = 0 # testes
		self.temporarios = []
		self.gato = Gato(150,self.height//2)
		self.gatos = []	# teste
		self.prepare_battle()

		# for i in range(6):
		# 	self.gatos.append(Gato(i*120, i*100))

	def input(self, keys):
		# Player Controls
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:		# move left
			if self.gato.x > 0:
				self.gato.movement_update(-1,0)
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:	# move right
			if self.gato.x < self.width:
				self.gato.movement_update(1,0)
		if keys[pygame.K_w] or keys[pygame.K_UP]:		# move up
			if self.gato.y > 0:
				self.gato.movement_update(0,-1)
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:		# move down
			if self.gato.y < self.height:
				self.gato.movement_update(0,1)
		if keys[pygame.K_SPACE] and self.gato.is_attack_ready():	# attack
			self.gato.attack(self.enemy)
		if keys[pygame.K_ESCAPE]:
			# self.running = False
			self.say_line()

	def logic(self):
		self.enemy.update()
		self.gato.update()
		self.credits.update()
		for g in self.gatos:
			g.update()
		for t in self.temporarios:
			t.update()

	def render(self, window):
		window.fill(self.background)		# background
		self.enemy.render(window)
		self.gato.render(window)
		for g in self.gatos:
			g.render(window)
		for t in self.temporarios:
			t.render(window)
		self.credits.render(window)			# credits
		pygame.display.update()				# update screen

	def wait_to_start(self):
		window = self.win
		x = self.width//2
		cor = (50,100,200)
		# titulo
		Text(x,100,"Aperte 'G' para iniciar",50,color=(50,250,50)).render(window)
		# textos
		textos = ["Use 'wasd' ou as setas para se mover",
				"Use 'espaco' para atacar",
				"Cuidado"]
		for i in range(3):
			Text(x,200+i*50,textos[i],40,color=cor).render(window)
		# creditos
		self.credits.render(window)
		pygame.display.update()
		# wait to player press 'g'
		while True:
			event = pygame.event.wait()
			if event.type == pygame.QUIT:	# kill screen
				self.running = False
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_g:	# start game
					break

def main():
	game = Gatinhos(800, 600, "Gatinhos")
	game.wait_to_start()		# wait to player press 'g'
	game.start()				# start game

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

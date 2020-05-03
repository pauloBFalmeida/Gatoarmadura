# coding: utf-8
import pygame
from random import randint
from time import sleep
from gato import Gato
from enemy import Enemy
from text import Text

pygame.init()

class Rinha_de_Gato:
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
		self.game_running = True
		self.FPS = 60
		self.background = (100, 120, 100)
		# frases
		self.frases = []
		with open('frases.txt') as file:
			 for line in file:
				 self.frases.append(line)

	def prepare_battle(self):
		# disable movement
		self.gato.move = False
		self.gato.attack_ready = False
		# create enemy
		right_direction = True
		if self.gato.x > self.width//2:	# player lado direito da tela
			right_direction = False
		self.enemy = Enemy(self.width-self.gato.x, self.height-self.gato.y, right_direction)
		self.enemy.move = False
		self.enemy.attack_ready = False
		# say the lines
		self.say_line()
		# start fight
		pygame.time.set_timer(pygame.USEREVENT+1, 2000)		# espera pra inciar

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
			self.temporarios.append(Text(x,
										y,
										select[j][:-1],	# texto
										20,
										color=(0,0,50),
										duration=self.FPS*2) )

	def start_battle(self):
		# start fight
		pygame.time.set_timer(pygame.USEREVENT+1, 0)		# espera pra inciar
		self.temporarios.append(Text(self.width//2,
									self.height//2,
									"Lutem",
									60,
									color=(250,50,50),
									duration=self.FPS*1))
		self.gato.start_battle(self.enemy)
		self.enemy.start_battle(self.gato)

	def start(self):
		self.enemies_defeated = 0
		self.temporarios = []
		self.gato = Gato(150,self.height//2-15, True)
		self.prepare_battle()

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
			self.gato.attack()
		if keys[pygame.K_ESCAPE]:
			# self.say_line()
			self.running = False

	def logic(self):
		self.enemy.update()
		self.gato.update()
		if not self.gato.vivo:
			self.running = False
		if not self.enemy.vivo:
			self.enemies_defeated += 1
			self.gato.coletar_armadura()
			self.prepare_battle()
		self.credits.update()
		for t in list(self.temporarios):
			t.update()
			if t.duration_ended(): self.temporarios.remove(t)

	def render(self, window):
		window.fill(self.background)		# background
		self.enemy.render(window)
		self.gato.render(window)
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
				"Cada gato comeca com 3 armaduras",
				"Porem voce coleta a armadura de inimigos derrotados",
				"Batalhem ate acabarem suas armaduras"]
		for i in range(5):
			Text(x,200+i*50,textos[i],30,color=cor).render(window)
		# creditos
		self.credits.render(window)
		pygame.display.update()
		# wait to player press 'g'
		while True:
			event = pygame.event.wait()
			if event.type == pygame.QUIT:	# kill screen
				self.running = False
				self.game_running = False
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_g:	# start game
					break

	def end_screen(self):
		window = self.win
		x = self.width//2
		cor = (50,100,200)
		# titulo
		Text(x,100,"Fim de jogo",50,color=(50,250,50)).render(window)
		# textos
		textos = ["Use 'G' para reiniciar",
				"Voce derrotou "+str(self.enemies_defeated)]
		for i in range(2):
			Text(x,200+i*100,textos[i],40,color=cor).render(window)
		# creditos
		self.credits.render(window)
		pygame.display.update()
		# wait to player press 'g'
		while True:
			event = pygame.event.wait()
			if event.type == pygame.QUIT:	# kill screen
				self.running = False
				self.game_running = False
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_g:	# start game
					self.running = True
					break

def main():
	game = Rinha_de_Gato(800, 600, "Rinha_de_Gato")

	game.wait_to_start()		# wait to player press 'g'
	while game.game_running:
		game.start()				# start game
		# loop
		while game.running:
			game.clock.tick(game.FPS)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game.running = False
					game.game_running = False
				elif event.type == pygame.USEREVENT+1:
					game.start_battle()

			game.input(pygame.key.get_pressed())
			game.logic()
			game.render(game.win)
		# end screen
		if game.game_running:
			game.end_screen()

if __name__ == "__main__":
	main()
	pygame.quit()
	quit()

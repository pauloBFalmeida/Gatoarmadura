import pygame
from random import randint
try: from PIL import Image
except: pass

class Manipulador():
	def __init__(self, size, arquivo, **kwargs):
		self.size = size
		self.cores = [self.random_color(), self.random_color()]	# detalhes, fundo
		for kwarg in kwargs.items():
			if kwarg[0] == 'detalhes':
				self.cores[0] = kwarg[1]
			if kwarg[0] == 'fundo':
				self.cores[1] = kwarg[1]
		self.image = self.generate_image(arquivo)

	def generate_image(self, arquivo):
		arquivo = "imagens/"+arquivo
		try:
			imgs = [None,None,None]
			imgs[0] = Image.open(arquivo+"_detalhes.png")
			imgs[1] = Image.open(arquivo+"_fundo.png")
			imgs[2] = Image.open(arquivo+"_borda.png")
			for i in range(3):
				imgs[i] = imgs[i].resize(self.size)
				imgs[i] = imgs[i].convert("RGBA")

			for i in range(2):
				imrgb = list(imgs[i].split())
				color = self.cores[i]
				for j in range(3):
					imrgb[j] = Image.eval(imrgb[j], (lambda p: self.colorise_image(p,color,j)) )
				imgs[i] = Image.merge("RGBA", imrgb)

			final_im = Image.alpha_composite(imgs[0], imgs[1])
			final_im = Image.alpha_composite(final_im, imgs[2])

			data = final_im.tobytes()
			return pygame.image.fromstring(data, final_im.size, final_im.mode)
		except:
			im = pygame.image.load(arquivo+".png")
			im = pygame.transform.scale(im, self.size)
			return im

	def colorise_image(self, pixel, color, i):
		margem = 20
		if pixel < (0+margem):
			return 0
		elif pixel > (255-margem):
			return color[i]
		else:
			return color[i]

	def random_color(self):
		return (randint(0,255),randint(0,255),randint(0,255))

	def get_cor_detalhes(self): return self.cores[0]
	def get_cor_fundo(self): return self.cores[1]

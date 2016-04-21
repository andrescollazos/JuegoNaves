import pygame 
from pygame.locals import *
import time
import sys
import random

ANCHO=600
ALTO=400
BLANCO=(255,255,255)

class Player(pygame.sprite.Sprite):
	def __init__(self, imagen):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagen).convert_alpha() #Cargar imagen
		self.rect = self.image.get_rect()
		self.lives = 3 # Vidas del jugador
		#self.shield = 0 # Escudo

	# Modificar posicion del jugador
	def set_pos(self, pos):
		self.rect.x = pos[0]
		self.rect.y = pos[1]

	# Actualizar el estado del jugador
	def update(self):
		pass

	# Realizar disparo
	def shot(self):
		pass

class Enemy(pygame.sprite.Sprite):
	def __init__(self, imagen):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagen).convert_alpha() #Cargar imagen
		self.rect = self.image.get_rect()
		self.lives = 2 # Vidas del enemigo

	# Modificar posicion del enemigo
	def set_pos(self, pos):
		self.rect.x = pos[0]
		self.rect.y = pos[1]

	# Actualizar el estado del enemigo
	def update(self):
		pass

	# Realizar disparo
	def shot(self):
		pass

class Bullet(pygame.sprite.Sprite):
	def __init__(self, imagen):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagen).convert_alpha() #Cargar imagen
		self.rect = self.image.get_rect()

	# Actualizar posicion de la bala
	def update(self):
		pass


if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode([ANCHO,ALTO])	
	background = pygame.image.load("images/background.jpg").convert_alpha()

	jugador = Player("images/playerShip1_red.png")

	ls_todos = pygame.sprite.Group()
	ls_todos.add(jugador)

	pygame.mouse.set_visible(False)
	terminar = False
	puntos = 0
	reloj = pygame.time.Clock()

	while not terminar:
		pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminar = True

		jugador.set_pos(pos)		
		screen.blit(background,(0,0))

		ls_todos.draw(screen)
		reloj.tick(60)
		pygame.display.flip()
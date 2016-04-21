import pygame
from pygame.locals import *
import time
import sys
import random

ANCHO = 800
ALTO = 600
BLANCO = (255,255,255)

# Imagenes de enemigos del primer nivel
enemys1 = [
		"images/Enemies/enemyBlack1.png",
		"images/Enemies/enemyBlue1.png",
		"images/Enemies/enemyGreen1.png",
		"images/Enemies/enemyRed1.png"
]

# Imangenes de enemigos del segundo nivel
enemys2 = [
		"images/Enemies/enemyBlack2.png",
		"images/Enemies/enemyBlue2.png",
		"images/Enemies/enemyGreen2.png",
		"images/Enemies/enemyRed2.png"
]

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
		self.direccion = 0 # Sentido del enemigo

	# Modificar posicion del enemigo
	def set_pos(self, pos):
		self.rect.x = pos[0]
		self.rect.y = pos[1]

	# Actualizar el estado del enemigo
	def update(self):
		self.rect.y += 1

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


def crearEnemigo():
	# Seleccionar un enemigo aleatorio
	e = random.randrange(0, len(enemys1))
	enemigo = Enemy(enemys1[e])
	enemigo.rect.x = random.randrange(ANCHO)
	enemigo.rect.y = random.randrange(-200, -20)
	return enemigo


if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode([ANCHO,ALTO])
	# Cargar imagen de fonod
	background = pygame.image.load("images/background.jpg").convert_alpha()

	# Crear un jugador
	jugador = Player("images/playerShip1_red.png")
	# Lista que va a contener todos los elementos
	ls_todos = pygame.sprite.Group()
	# Lista que contiene todos los enemigos
	ls_enemigo = pygame.sprite.Group()

	# Crear enemigos
	for i in range(10):
		e = crearEnemigo()
		ls_enemigo.add(e)
		ls_todos.add(e)
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

		ls_todos.update()
		ls_todos.draw(screen)
		reloj.tick(60)
		pygame.display.flip()

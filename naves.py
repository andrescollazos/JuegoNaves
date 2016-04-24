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

# ------------------------------------------------------------------------------
# CLASE JUGADOR
#-------------------------------------------------------------------------------
class Jugador(pygame.sprite.Sprite):
	def __init__(self, imagen):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagen).convert_alpha() #Cargar imagen
		self.rect = self.image.get_rect()
		self.vidas = 3 # Vidas del jugador
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
# ------------------------------------------------------------------------------
# CLASE ENEMIGO
#-------------------------------------------------------------------------------

class Enemigo(pygame.sprite.Sprite):
	def __init__(self, imagen):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagen).convert_alpha() #Cargar imagen
		self.rect = self.image.get_rect()
		self.vidas = 2 # Vidas del enemigo
		self.direccion = 0 # Sentido del movimiento del enemigo
		self.disparar = False
		self.recarga = 100

	# Modificar posicion del enemigo
	def set_pos(self, pos):
		self.rect.x = pos[0]
		self.rect.y = pos[1]

	# Actualizar el estado del enemigo
	def update(self):
		if self.rect.x <= 0:
			self.direccion = 1
			self.rect.y += 16
		if self.rect.x >= (ANCHO - 32):
			self.direccion = 0
			self.rect.y += 16

		if self.direccion == 1:
			self.rect.x += 10
		else:
			self.rect.x -= 10

		# Disparar
		if self.recarga == 0:
			if self.rect.y > -84: # 84 es la altura de la nave enemiga
				self.recarga = random.randrange(100)
				self.disparar = True
		else:
			self.recarga -= 1

# ------------------------------------------------------------------------------
# CLASE BALA
#-------------------------------------------------------------------------------

class Bala(pygame.sprite.Sprite):
	def __init__(self, imagen, posicion):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagen).convert_alpha() #Cargar imagen
		self.rect = self.image.get_rect()
		self.rect.x = posicion[0]
		self.rect.y = posicion[1]
		self.bando = 0 # Sentido en el que se dirige la bala

	# Actualizar posicion de la bala
	def update(self):
		if self.bando == 1: # Bando -> 1, bala disparada por el enemigo
			self.rect.y += 5
		else:
			self.rect.y -= 5 # Bala disparada por el jugador

# ------------------------------------------------------------------------------
# FUNCIONES
#-------------------------------------------------------------------------------

# lvl es el nivel en el que esta el jugador
def crearEnemigo(lvl):
	# Seleccionar un enemigo aleatorio
	e = random.randrange(0, len(enemys1))
	if lvl == 1:
		enemigo = Enemigo(enemys1[e])
	elif lvl == 2:
		enemigo = Enemigo(enemys2[e])
	enemigo.rect.x = random.randrange(ANCHO)
	enemigo.rect.y = random.randrange(-252, -84)
	return enemigo


if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode([ANCHO,ALTO])
	# Cargar imagen de fondo
	fondo = pygame.image.load("images/background.jpg").convert_alpha()

	# Crear un jugador
	jugador = Jugador("images/playerShip1_red.png")
	ls_jugador = pygame.sprite.Group() # para analizar las colisiones con las balas
	# Lista que va a contener todos los elementos
	ls_todos = pygame.sprite.Group()
	# Lista que contiene todos los enemigos
	ls_enemigo = pygame.sprite.Group()
	# Lista que contiene las balas disparadas por el jugador
	ls_balas = pygame.sprite.Group()
	# Lista que contiene las balas disparadas por el enemigo
	ls_ebalas = pygame.sprite.Group()

	# Crear enemigos
	for i in range(2):
		e = crearEnemigo(1)
		ls_enemigo.add(e)
		ls_todos.add(e)
	ls_jugador.add(jugador)
	ls_todos.add(jugador)

	# Mouse invisible
	pygame.mouse.set_visible(False)
	terminar = False
	# Un punto representa un impacto a un enemigo
	puntos = 0
	reloj = pygame.time.Clock()

	while not terminar:
		pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminar = True
			# Disparo del juador
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Boton izquierdo del mouse
				if pygame.mouse.get_pressed()[0] == 1:
					bala = Bala('images/Lasers/laserBlue01.png', [pos[0]+45, pos[1]])
					ls_balas.add(bala)
					ls_todos.add(bala)

		# La posicion del jugador la define la posicion del mouse
		jugador.set_pos(pos)
		screen.blit(fondo,(0,0))

		# Nave enemiga es destruida por el impacto de la bala
		for e in ls_enemigo:
			ls_impactos = pygame.sprite.spritecollide(e, ls_balas, True)
			for imp in ls_impactos:
				e.vidas -=1 #Por cada impacto la vida del enemigo disminuye en 1
				if e.vidas == 0:
					ls_enemigo.remove(e)
					ls_todos.remove(e)
				puntos += 1
				print "PUNTAJE: ", puntos

		# Bala enemigo impacta con el jugador
		for eb in ls_ebalas:
			impactado = pygame.sprite.spritecollide(eb, ls_jugador, False)
			for imp in impactado:
				# Impacto de bala enemiga reduce la vida del jugador en 1
				jugador.vidas -= 1
				# Cuando las vidas llegan a 0, se termina el juego
				if jugador.vidas < 0:
					terminar = True
					print "FIN DEL JUEGO"
				ls_ebalas.remove(eb)
				ls_todos.remove(eb)

		ls_todos.update()

		# DISPARO DE LOS ENEMIGOS
		for enemigo in ls_enemigo:
			if enemigo.disparar:
				x = enemigo.rect.x + 5
				y = enemigo.rect.y + 32
				bala = Bala('images/Lasers/laserRed01.png', [x,y])
				bala.bando = 1
				ls_ebalas.add(bala)
				ls_todos.add(bala)
				enemigo.disparar = False

		ls_todos.draw(screen)
		reloj.tick(60)
		pygame.display.flip()

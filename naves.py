# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import time
import sys
import random
import caminos

ANCHO = 800
ALTO = 600
BLANCO = (255,255,255)

# Imagenes de los numeros del marcador
num_marcador = [
		"images/UI/numeral0.png",
		"images/UI/numeral1.png",
		"images/UI/numeral2.png",
		"images/UI/numeral3.png",
		"images/UI/numeral4.png",
		"images/UI/numeral5.png",
		"images/UI/numeral6.png",
		"images/UI/numeral7.png",
		"images/UI/numeral8.png",
		"images/UI/numeral9.png",
		"images/UI/numeralx.png",	# ICONO 'X'
		"images/UI/cursor.png",		# ICONO DE PUNTOS
		"images/UI/playerLife.png"	# ICONO VIDA DEL JUGADOR
]


# Imagenes de enemigos del primer nivel
enemigos1 = [
		"images/Enemies/enemyBlack1.png",
		"images/Enemies/enemyBlue1.png",
		"images/Enemies/enemyGreen1.png",
		"images/Enemies/enemyRed1.png"
]

# Imangenes de enemigos del segundo nivel
enemigos2 = [
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
		#self.vidas = 3 # Vidas del jugador
		#self.shield = 0 # Escudo
		#self.marcador = None # Colision JUGADOR - MARCADOR

	# Modificar posicion del jugador
	def set_pos(self, pos):
		self.rect.x = pos[0]
		self.rect.y = pos[1]

	# Actualizar el estado del jugador
	def update(self):
		pass

	# Realizar disparo
	def shot(self, ls_balas, ls_todos):
		bala = Bala('images/Lasers/laserBlue01.png',[self.rect.x+45, self.rect.y])
		ls_balas.add(bala)
		ls_todos.add(bala)
		return ls_balas, ls_todos
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
		self.pos_j = 0 # Posicion(jugador) a la cual se dirige la bala
		self.trayectoria = [] # Trayectoria desde la nave al jugador
	# Actualizar posicion de la bala
	def update(self):
		if self.pos_j != 0: # Bala disparada por enemigo
			self.rect.y += 5
		else:
			self.rect.y -= 5 # Bala disparada por el jugador

# ------------------------------------------------------------------------------
# CLASE MARCADOR
#-------------------------------------------------------------------------------
class Simbolo(pygame.sprite.Sprite):
	def __init__(self, image, simbolo, posicion):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = posicion[0]
		self.rect.y = posicion[1]
		# Se requiere saber la posicion para actualizarlo (cargar otra imagen)
		self.pos = posicion # Esta nunca cambia
		self.simbolo = simbolo
	def update(self):
		# Cargar la imagen para cada simbolo
		if self.simbolo == 0:
			self.image = pygame.image.load(num_marcador[0]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 1:
			self.image = pygame.image.load(num_marcador[1]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 2:
			self.image = pygame.image.load(num_marcador[2]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 3:
			self.image = pygame.image.load(num_marcador[3]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 4:
			self.image = pygame.image.load(num_marcador[4]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 5:
			self.image = pygame.image.load(num_marcador[5]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 6:
			self.image = pygame.image.load(num_marcador[6]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 7:
			self.image = pygame.image.load(num_marcador[7]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 8:
			self.image = pygame.image.load(num_marcador[8]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 9:
			self.image = pygame.image.load(num_marcador[9]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 'x':
			self.image = pygame.image.load(num_marcador[10]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 'vida':
			self.image = pygame.image.load(num_marcador[12]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.simbolo == 'puntos':
			self.image = pygame.image.load(num_marcador[11]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]

# ------------------------------------------------------------------------------
# FUNCIONES
#-------------------------------------------------------------------------------
# ej: aumentar_puntaje(0) -> [0, 0, 1]
# ej: aumentar_puntaje(9) -> [0, 1, 0]
# ej: aumentar_puntaje(99) ->[1, 0, 0]
def aumentar_puntaje(puntos):
	puntos = puntos + 1
	d1 = puntos%10
	d2 = (puntos%100)/10
	d3 = (puntos%1000)/100
	return [d1, d2, d3]

# lvl es el nivel en el que esta el jugador
def crearEnemigo(lvl):
	# Seleccionar un enemigo aleatorio
	e = random.randrange(0, len(enemigos1))
	if lvl == 1:
		enemigo = Enemigo(enemigos1[e])
	elif lvl == 2:
		enemigo = Enemigo(enemigos2[e])
	enemigo.rect.x = random.randrange(ANCHO)
	enemigo.rect.y = random.randrange(-252, -84)
	return enemigo


if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode([ANCHO,ALTO])
	# Cargar imagen de fondo
	fondo = pygame.image.load("images/background.jpg").convert_alpha()

	# Marcador:
	# El marcador consiste: Uu digito para la vida y el escudo, tres digitos
	# los puntos

	# Vida del jugador
	icono_vida 	= Simbolo(num_marcador[12], 'vida',[10,570])
	icono_xv 	= Simbolo(num_marcador[10], 'x', [57, 570])
	vida 		= Simbolo(num_marcador[9], 9, [84, 570])
	# Puntaje
	icono_puntos= Simbolo(num_marcador[11], 'puntos', [666, 570])
	icono_xp	= Simbolo(num_marcador[10], 'x', [706, 570])
	puntos 		= 0
	punt0 		= Simbolo(num_marcador[0], 0, [771, 570])
	punt1		= Simbolo(num_marcador[0], 0, [752, 570])
	punt2		= Simbolo(num_marcador[0], 0, [733, 570])

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
	for i in range(10):
		e = crearEnemigo(1)
		ls_enemigo.add(e)
		ls_todos.add(e)
	# Agregar sprites a la lista de todos los elementos
	# Sprite del jugador
	ls_jugador.add(jugador)
	ls_todos.add(jugador)
	# Sprites de vida
	ls_todos.add(vida)
	ls_todos.add(icono_vida)
	ls_todos.add(icono_xv)
	# Sprites de puntos
	ls_todos.add(punt0)
	ls_todos.add(punt1)
	ls_todos.add(punt2)
	ls_todos.add(icono_puntos)
	ls_todos.add(icono_xp)

	# Mouse invisible
	pygame.mouse.set_visible(False)
	terminar = False
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
					jugador.shot(ls_balas, ls_todos)

		# La posicion del jugador la define la posicion del mouse
		jugador.set_pos(pos)
		screen.blit(fondo,(0,0))

		# Nave enemiga es destruida por el impacto de la bala
		if len(ls_enemigo) == 0:
			terminar = True
			print "VICTORIA"

		for e in ls_enemigo:
			ls_impactos = pygame.sprite.spritecollide(e, ls_balas, True)
			for imp in ls_impactos:
				if e.rect.y > 0 - 83:	# La bala del jugador daña, solamente
										# cuando el enemigo es visible
					e.vidas -=1 #Por cada impactovida del enemigo disminuye en 1
					if e.vidas == 0:
						ls_enemigo.remove(e)
						ls_todos.remove(e)
					# Un punto representa un impacto a una nave enemiga
					p = aumentar_puntaje(puntos)
					punt0.simbolo = p[0]
					punt1.simbolo = p[1]
					punt2.simbolo = p[2]
					puntos += 1
					print "PUNTAJE: ", puntos

		# Bala enemigo impacta con el jugador
		for eb in ls_ebalas:
			impactado = pygame.sprite.spritecollide(eb, ls_jugador, False)
			for imp in impactado:
				# Impacto de bala enemiga reduce la vida del jugador en 1
				vida.simbolo -= 1
				# Cuando las vidas llegan a 0, se termina el juego
				if vida.simbolo < 0:
					terminar = True
					#ls_todos.remove(jugador)
					print "FIN DEL JUEGO"
				ls_ebalas.remove(eb)
				ls_todos.remove(eb)

		ls_todos.update()

		# DISPARO DE LOS ENEMIGOS
		for enemigo in ls_enemigo:
			# El enemigo solo empieza a disparar cuando este es visible
			if enemigo.rect.y > 0 - 84: #84 -> altura del enemigo
				if enemigo.disparar:
					x = enemigo.rect.x + 5
					y = enemigo.rect.y + 32
					#bala = Bala('images/Lasers/laserRed01.png', [x,y])
					bala = Bala('images/Lasers/laserRed01.png', [x,y])
					bala.pos_j = pos # La bala se apunta al jugador
					ls_ebalas.add(bala)
					ls_todos.add(bala)
					enemigo.disparar = False

		# LAS BALAS QUE HAYAN SALIDO DE LA PANTALLA YA NO SON TENIDAS EN CUENTA
		for eb in ls_ebalas:
			if eb.rect.x < 0 or eb.rect.x > ANCHO or eb.rect.y > ALTO:
				ls_ebalas.remove(eb)
				ls_todos.remove(eb)

		ls_todos.draw(screen)
		reloj.tick(60)
		pygame.display.flip()

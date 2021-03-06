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
		"images/UI/playerLife.png",	# ICONO VIDA DEL JUGADOR
		"images/UI/pildora.png",	# PODER DE PILDORA (SALUD)
		"images/UI/escudo.png",		# PODER DE ESCUDO
		"images/UI/icono_escudo.png"# ICONO DE ESCUDO
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
		self.vidas = 1 # Vidas del enemigo
		self.nivel = 1 # Nivel del enemigo
		self.direccion = 0 # Sentido del movimiento del enemigo
		self.velocidad = 0 # Velocidad del enemigo
		self.disparar = False
		self.recarga = 100
		self.recargaFijo = 100
		self.trayectoria = [] # Trayectoria en la que se mueve enemigo (lvl 2)
		self.cont = 0 # contador para recorrer trayectoria

	# Modificar posicion del enemigo
	#def set_pos(self, pos):
	#	self.rect.x = pos[0]
	#	self.rect.y = pos[1]

	# Actualizar el estado del enemigo
	def update(self):
		if self.nivel == 1:
			if self.rect.x <= 0:
				self.direccion = 1
				self.rect.y += self.velocidad
			if self.rect.x >= (ANCHO - self.rect[2]):
				self.direccion = 0
				self.rect.y += self.velocidad

			if self.direccion == 1:
				self.rect.x += self.velocidad + 5
			else:
				self.rect.x -= self.velocidad + 5
		elif self.nivel == 2:
			if self.cont == len(self.trayectoria)-4:
				self.trayectoria = caminos.espiral(self.trayectoria, 30)
				self.cont = 0
			else:
				self.rect.x = self.trayectoria[self.cont][0]
				self.rect.y = self.trayectoria[self.cont][1]
				self.cont += 5

		# Disparar
		if self.recarga == 0:
			# La nave empieza a disparar cuando es visible en pantalla
			if self.rect.y > -1*self.rect[3]: # Altura de la nave enemiga
				self.recarga = random.randrange(self.recargaFijo) # Velocidad de disparo
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
		self.velocidad = 5 # Valor a ser modificado
		self.pos_j = 0 # Posicion(jugador) a la cual se dirige la bala
		self.trayectoria = [] # Trayectoria desde la nave al jugador
		self.cont = 0 # para moverse por el vector de trayectoria
	# Actualizar posicion de la bala
	def update(self):
		if self.pos_j != 0: # Bala disparada por enemigo
			self.rect.x = self.trayectoria[self.cont][0]
			self.rect.y = self.trayectoria[self.cont][1]
			self.cont += self.velocidad # velocidad de la bala
		else:
			self.rect.y -= self.velocidad # Bala disparada por el jugador

# ------------------------------------------------------------------------------
# CLASE MARCADOR
#-------------------------------------------------------------------------------
class Icono(pygame.sprite.Sprite):
	def __init__(self, image, valor, posicion):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = posicion[0]
		self.rect.y = posicion[1]
		# Se requiere saber la posicion para actualizarlo (cargar otra imagen)
		self.pos = posicion # Esta nunca cambia
		self.valor = valor
	def update(self):
		# Cargar la imagen para cada simbolo
		if self.valor == 0:
			self.image = pygame.image.load(num_marcador[0]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 1:
			self.image = pygame.image.load(num_marcador[1]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 2:
			self.image = pygame.image.load(num_marcador[2]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 3:
			self.image = pygame.image.load(num_marcador[3]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 4:
			self.image = pygame.image.load(num_marcador[4]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 5:
			self.image = pygame.image.load(num_marcador[5]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 6:
			self.image = pygame.image.load(num_marcador[6]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 7:
			self.image = pygame.image.load(num_marcador[7]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 8:
			self.image = pygame.image.load(num_marcador[8]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 9:
			self.image = pygame.image.load(num_marcador[9]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 'x':
			self.image = pygame.image.load(num_marcador[10]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 'vida':
			self.image = pygame.image.load(num_marcador[12]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 'puntos':
			self.image = pygame.image.load(num_marcador[11]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 'escudo':
			self.image = pygame.image.load(num_marcador[14]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 'icono_escudo':
			self.image = pygame.image.load(num_marcador[15]).convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
		elif self.valor == 'pildora':
			self.image = pygame.image.load(num_marcador[13]).convert_alpha()
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
# i -> en que tanda sale el enemigo
def crearEnemigo(lvl, i):
	# Seleccionar un enemigo aleatorio (color)
	e = random.randrange(0, len(enemigos1))
	if lvl == 1:
		enemigo = Enemigo(enemigos1[e])
	elif lvl == 2:
		enemigo = Enemigo(enemigos2[e])
	enemigo.rect.x = random.randrange(84, ANCHO-84)
	# enemigo.rect[3] -> Altura del enemigo
	# El enemigo aparece aleatoriamente por encima del area visible
	if lvl == 2:
		i *= 3
	enemigo.rect.y = -1*enemigo.rect[3]*(i*0.7)
	return enemigo

# Funcion que retorna la trayectoria que seguirá la bala hasta el Jugador
def btrayectoria(e, j): # b-> posicion nave enemiga al momento de disparar
	m = (e[1] - j[1])/(e[0] - j[0])
	b = e[1] - m*e[0]
	if j[0] < e[0]:
		x = j[0] - ANCHO*2
	elif j[0] > e[0]:
		x = j[0] + ANCHO*2
	elif j[0] == e[0]:
		x = j[0]
	y = m*x + b
	trayectoria = caminos.linea(e, (x,y))
	return trayectoria
# ------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------
if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode([ANCHO,ALTO])
	# Cargar imagenes de fondo (imagenes de dominio publico)
	fondo1 = pygame.image.load("images/fondos/background.jpg").convert_alpha()
	fondo2 = pygame.image.load("images/fondos/background2.jpg").convert_alpha()
	lvlcomp = pygame.image.load("images/fondos/nivelcompletado.jpg").convert_alpha()
	vict = pygame.image.load("images/fondos/victoria.jpg").convert_alpha()
	derr = pygame.image.load("images/fondos/derrota.jpg").convert_alpha()

	# ICONOS
	# Vida del jugador
	icono_vida 	= Icono(num_marcador[12], 'vida',[10,ALTO-30])
	icono_xv 	= Icono(num_marcador[10], 'x', [57, ALTO-30])
	vida 		= Icono(num_marcador[9], 9, [84, ALTO-30])
	# Puntaje
	icono_puntos= Icono(num_marcador[11], 'puntos', [ANCHO-131, ALTO-30])
	icono_xp	= Icono(num_marcador[10], 'x', [ANCHO-88, ALTO-30])
	puntos 		= 0
	punt0 		= Icono(num_marcador[0], 0, [ANCHO-27, ALTO-30])
	punt1		= Icono(num_marcador[0], 0, [ANCHO-44, ALTO-30])
	punt2		= Icono(num_marcador[0], 0, [ANCHO-61, ALTO-30])
	# Poderes
	icono_escudo= Icono(num_marcador[15], 'icono_escudo', [123, ALTO-30])
	icono_xe 	= Icono(num_marcador[10], 'x', [163, ALTO-30])
	escudo = Icono(num_marcador[0], 0, [190, ALTO-30])
	esc = Icono(num_marcador[14], 'escudo', [0, 0])
	pildora = Icono(num_marcador[13], 'pildora', [0, 0])
	pbandera = False # Indica si hay un poder o no en pantalla
	# --------------------------------------------------------------------------
	# Nivel de juego
	#---------------------------------------------------------------------------
	nivel = Icono(num_marcador[1], 1, [10, 10])
	edestruidos = 0
	emax1 = 20 # Cantidad de enemigos del Nivel 1
	emax2 = 30 # Cantidad de enemigos del Nivel 2

	# Crear un jugador
	jugador = Jugador("images/playerShip1_red.png")

	# Grupos
	# Lista para analizar las colisiones con las balas
	ls_jugador = pygame.sprite.Group()
	# Lista que va a contener todos los elementos
	ls_todos = pygame.sprite.Group()
	# Lista que contiene todos los enemigos
	ls_enemigo = pygame.sprite.Group()
	# Lista que contiene las balas disparadas por el jugador
	ls_balas = pygame.sprite.Group()
	# Lista que contiene las balas disparadas por el enemigo
	ls_ebalas = pygame.sprite.Group()
	# Lista que contiene los poderes que estan en pantalla
	ls_poderes = pygame.sprite.Group()

	# Los enemigos ahora son creados en el ciclo principal del juego

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
	# Sprites escudo
	ls_todos.add(icono_escudo)
	ls_todos.add(icono_xe)
	ls_todos.add(escudo)
	# Sprites nivel
	ls_todos.add(nivel)

	# Mouse invisible
	pygame.mouse.set_visible(False)
	crear = True # Booleano que permite saber si crear o no enemigos
	terminar = False
	# Para mostrar una imagen de victoria
	victoria = False
	# Para mostrar una imagen de derrota
	derrota = False
	reloj = pygame.time.Clock()

	while not terminar:
		# Crear enemigos
		if crear:
			if nivel.valor == 1:
				emax = emax1
			elif nivel.valor == 2:
				emax = emax2
			j = 1
			for i in range(emax):
				if i == 3*j:
					j += 1
				e = crearEnemigo(nivel.valor, j)
				e.vidas = nivel.valor + 1 # Vidas del enemigo
				e.nivel = nivel.valor
				e.recargaFijo = 100 - 5*nivel.valor
				e.velocidad = 7*nivel.valor
				# RECORRIDO EN CIRCUNFERENCIA (LVL2)
				x, y = e.rect.x, e.rect.y
				e.trayectoria = caminos.circunferencia((x, y), 100)
				ls_enemigo.add(e)
				ls_todos.add(e)
			crear = False

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
		if nivel.valor == 1:
			screen.blit(fondo1,(0,0))
		elif nivel.valor == 2:
			screen.blit(fondo2,(0,0))

		# El jugador toma un PODER
		# POSICION ALEATORIA DONDE APARECERÁ EL PODER
		xp = random.randrange(30, ANCHO-30)
		yp = random.randrange(30, ALTO-30)
		# CANTIDAD MAXIMA DE PODER A CAPTURAR
		escmax = 9 # Siempre es 9
		pildoramax = 9 # Siempre es 9
		 # PROBABILIDAD (aprox) DE QUE SALGA UN PODER-> nivel.valor/1000
		poder = random.randrange(1000/nivel.valor)
		if poder == 27 and pbandera == False: #27 -> numero aleatorio
			sel = random.randrange(2)
			if sel == 0: # Escudo
				esc.pos = [xp, yp]
				ls_todos.add(esc)
				ls_poderes.add(esc)
			elif sel == 1: # Pildora (Vida)
				pildora.pos = [xp, yp]
				ls_todos.add(pildora)
				ls_poderes.add(pildora)
			pbandera = True

		for p in ls_poderes:
			capturado = pygame.sprite.spritecollide(p, ls_jugador, False)
			for cap in capturado:
				if p.valor == 'escudo':
					if escudo.valor < escmax:
						escudo.valor += 1
				elif p.valor == 'pildora':
					if vida.valor < pildoramax:
						vida.valor += 1
				ls_todos.remove(p)
				ls_poderes.remove(p)
				pbandera = False

		# Nave enemiga es destruida por el impacto de la bala
		for e in ls_enemigo:
			ls_impactos = pygame.sprite.spritecollide(e, ls_balas, True)
			for imp in ls_impactos:
				# La bala del jugador daña, solamente
				# cuando el enemigo es visible
				if e.rect.y > -1*(e.rect[3] - 1):
					e.vidas -=1 #Por cada impactovida del enemigo disminuye en 1
					if e.vidas == 0:
						ls_enemigo.remove(e)
						ls_todos.remove(e)
					# Un punto representa un impacto a una nave enemiga
					p = aumentar_puntaje(puntos)
					punt0.valor = p[0]
					punt1.valor = p[1]
					punt2.valor = p[2]
					puntos += 1
					print "PUNTAJE: ", puntos

		# Evaluar si el jugador termino un nivel o si gano el juego
		if len(ls_enemigo) == 0:
			if nivel.valor == 1:
				crear = True
				nivel.valor = 2
			elif nivel.valor == 2:
				#terminar = True
				victoria = True
				print "VICTORIA"

		# Bala enemigo impacta con el jugador
		for eb in ls_ebalas:
			impactado = pygame.sprite.spritecollide(eb, ls_jugador, False)
			for imp in impactado:
				if escudo.valor > 0:
					escudo.valor -= 1
				else:
					# Impacto de bala enemiga reduce la vida del jugador en 1
					vida.valor -= 1
					# Cuando las vidas llegan a 0, se termina el juego
					if vida.valor < 0:
						#terminar = True
						derrota = True
						print "FIN DEL JUEGO"
				ls_ebalas.remove(eb)
				ls_todos.remove(eb)

		ls_todos.update()

		# DISPARO DE LOS ENEMIGOS
		for enemigo in ls_enemigo:
			# El enemigo solo empieza a disparar cuando este es visible
			if enemigo.rect.y > -1*(enemigo.rect[3]): # Altura del enemigo
				if enemigo.disparar:
					# El disparo sale de la mitad de la nave enemiga
					x = enemigo.rect.x + (enemigo.rect[2]/2)
					y = enemigo.rect.y + (enemigo.rect[3]/2)
					bala = Bala('images/Lasers/laserRed01.png', [x,y])
					bala.pos_j = pos # La bala se apunta al jugador
					# Trayectoria de la bala hasta el jugador:
					bala.trayectoria = btrayectoria((x,y), pos)
					bala.velocidad = nivel.valor*6 # velocidad: n1-> 6  n2-> 12
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

		# EN CASO DE PASAR DE NIVEL 0 VICTORIA O DERROTA :
		if crear:
			# Esperar cinco segundos
			pygame.time.wait(3000)
			screen.blit(lvlcomp,(0,0))
			pygame.display.flip()
			pygame.time.wait(3000)
		if victoria:
			# Esperar cinco segundos
			pygame.time.wait(3000)
			screen.blit(vict,(0,0))
			pygame.display.flip()
			pygame.time.wait(3000)
			terminar = True
		if derrota:
			# Esperar cinco segundos
			pygame.time.wait(3000)
			screen.blit(derr,(0,0))
			pygame.display.flip()
			pygame.time.wait(3000)
			terminar = True

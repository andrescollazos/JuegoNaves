import pygame
import sys
#-------------------------------------------------------------------------------
# ALGORITMO DE PUNTO MEDIO - BRESENHAM PARA LINEA
#-------------------------------------------------------------------------------
def linea(p1, p2):
	puntos = []
	dx = (p2[0] - p1[0])
	dy = (p2[1] - p1[1])
	# Determinar que punto usar para empezar y cual para terminar.
	if dy < 0:
		dy = -dy
		stepy = -1
	else:
		stepy = 1
	if dx < 0:
		dx = -dx
		stepx = -1
	else:
		stepx = 1

	x = p1[0]
	y = p1[1]
	# Bucle hasta llegar al otro extremo de la linea.
	if dx > dy:
		p = 2*dy-dx
		while x != p2[0]:
			x += stepx
			if p < 0:
				p += 2*dy
			else:
				y += stepy
				p += 2*(dy-dx)
			#pantalla.set_at((x, y), color)
			puntos.append((x, y))
	else:
		p = 2*dx-dy
		while y != p2[1]:
			y = y + stepy
			if p < 0:
				p += 2*dx
			else:
				x += stepx
				p += 2*(dx-dy)
			#pantalla.set_at((x, y), color)
			puntos.append((x, y))
	return puntos

#-------------------------------------------------------------------------------
# ALGORITMO DE PUNTO MEDIO - BRESENHAM PARA CIRCUNFERENCIA
#-------------------------------------------------------------------------------
# En la carpeta PNG esta el diagrama que muestra la division de la cirncunferencia
# por octantes -> /images/division_circ.png
def simetricos(pantalla, color, vc, v):
	xc, yc = vc[0], vc[1]
	x, y = v[0], v[1]
	pantalla.set_at((xc + x, yc + y), color) # 1
	pantalla.set_at((xc - x, yc + y), color) # 2
	pantalla.set_at((xc + x, yc - y), color) # 3
	pantalla.set_at((xc - x, yc - y), color) # 4
	pantalla.set_at((xc + y, yc + x), color) # 5
	pantalla.set_at((xc - y, yc + x), color) # 6
	pantalla.set_at((xc + y, yc - x), color) # 7
	pantalla.set_at((xc - y, yc - x), color) # 8

def circunferencia(pantalla, color, centro, radio):
	x = 0
	y = radio
	d = 1 - y
	simetricos(pantalla, color, centro, (x, y))
	while y > x:
		if d < 0:
			d = d + 2*x + 1
		else:
			d = d + 2*(x - y) + 1
			y = y - 1
		x = x + 1
		simetricos(pantalla, color, centro, (x,y))

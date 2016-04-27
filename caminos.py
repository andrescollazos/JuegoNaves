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
def simetricos(vc, v, octantes):
	xc, yc = vc[0], vc[1]
	x, y = v[0], v[1]
	#pantalla.set_at((xc + x, yc + y), color) # 1
	octantes[0].append((xc + x, yc + y))
	#pantalla.set_at((xc - x, yc + y), color) # 2
	octantes[1].append((xc - x, yc + y))
	#pantalla.set_at((xc + x, yc - y), color) # 3
	octantes[2].append((xc + x, yc - y))
	#pantalla.set_at((xc - x, yc - y), color) # 4
	octantes[3].append((xc - x, yc - y))
	#pantalla.set_at((xc + y, yc + x), color) # 5
	octantes[4].append((xc + y, yc + x))
	#pantalla.set_at((xc - y, yc + x), color) # 6
	octantes[5].append((xc - y, yc + x))
	#pantalla.set_at((xc + y, yc - x), color) # 7
	octantes[6].append((xc + y, yc - x))
	#pantalla.set_at((xc - y, yc - x), color) # 8
	octantes[7].append((xc - y, yc - x))

def circunferencia(centro, radio):
	octantes = [[], [], [], [], [], [], [], []]
	x = 0
	y = radio
	d = 1 - y
	simetricos(centro, (x, y), octantes)
	while y > x:
		if d < 0:
			d = d + 2*x + 1
		else:
			d = d + 2*(x - y) + 1
			y = y - 1
		x = x + 1
		simetricos(centro, (x,y), octantes)
	# Ordenar la circunferencia:
	o5 = octantes[4]
	o5.reverse()
	o7 = octantes[6]
	o3 = octantes[2]
	o3.reverse()
	o4 = octantes[3]
	o8 = octantes[7]
	o8.reverse()
	o6 = octantes[5]
	o2 = octantes[1]
	o2.reverse()
	o1 = octantes[0]
	return o5 + o7 + o3 + o4 + o8 + o6 + o2 + o1

def espiral(trayectoria, bajada):
	nueva = []
	for i in trayectoria:
		x = i[0]
		y = i[1] + bajada
		nueva.append((x,y))
	return nueva

#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea los conectivos
conectivos = ['Y', 'O', '>', '=']
# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def String2Tree(A):
	# Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
	# Input: - A, lista de caracteres con una formula escrita en notacion polaca inversa
	#        - letrasProposicionales, lista de letras proposicionales
	#        - conectivos, lista de conectivos
	# Output: formula como tree
	pila = []
	for c in A:
		# print("Examinando " + str(c))
		if c in letrasProposicionales:
			# print(u"El símbolo es letra proposicional")
			pila.append(Tree(c, None, None))
		elif c == '-':
			# print("Negamos")
			formulaAux = Tree(c, None, pila[-1])
			del pila[-1]
			pila.append(formulaAux)
		elif c in conectivos:
			# print("Unimos mediante conectivo")
			formulaAux = Tree(c, pila[-1], pila[-2])
			del pila[-1]
			del pila[-1]
			pila.append(formulaAux)
		else:
			print(u"Hay un problema: el símbolo " + str(c) + " no se reconoce")
	return pila[-1]

def Inorder2Tree(A):
	if len(A) == 1:
		return Tree(A[0], None, None)
	elif A[0] == '-':
		return Tree(A[0], None, Inorder2Tree(A[1:]))
	elif A[0] == "(":
		counter = 0 #Contador de parentesis
		for i in range(1, len(A)):
			if A[i] == "(":
				counter += 1
			elif A[i] == ")":
				counter -=1
			elif (A[i] in ['Y', 'O', '>', '=']) and (counter == 0):
				return Tree(A[i], Inorder2Tree(A[1:i]), Inorder2Tree(A[i + 1:-1]))
	else:
		return -1

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"

def imprime_listaHojas(L):
	for h in L:
		print(imprime_hoja(h))

def complemento(l):
	# Esta función devuelve el complemento de un literal
	# Input: l, un literal
	# Output: x, un literal
  if(l.label=='-'):
    return l.right
  elif(l.label!='-'):
    return Tree('-', None, l)

def par_complementario(l):
	# Esta función determina si una lista de solo literales
	# contiene un par complementario
	# Input: l, una lista de literales
	# Output: True/False
    y = [Inorder(i)for i in l]
    for i in l:
        if Inorder(complemento(i)) in y:
            return True

    return False

def es_literal(f):
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
  if(f.label in letrasProposicionales):
    return True
  elif(f.label == '-' and f.right.label in letrasProposicionales):
    return True
  else:
    return False

def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
	for i in l:
		if(es_literal(i)==False):
			return "No hay solo literales"

def clasificacion(f):
	# clasifica una fórmula como alfa o beta
	# Input: f, una fórmula como árbol
	# Output: string de la clasificación de la formula
	if(f.label=='-'):
		#clasificacion para alfas '-'
		if(f.right.label=='-'):
			if(f.right.right.label=='-'):
				return "!ERROR¡"
			return "1ALFA"
		elif(f.right.label=='O'):
			return "3ALFA"
		elif(f.right.label=='>'):
			return "4ALFA"
		#clasificacion para beta '-'
		elif(f.right.label=='Y'):
			return "1BETA"
		else:
			return "!ERROR EN LA CLASIFICACION¡"
		#clasificacion para las que no aplican
		
	elif(f.label=='Y'):
		return "2ALFA"
	elif(f.label=='O'):
		return "2BETA"
	elif(f.label=='>'):
		return "3BETA"
	

def clasifica_y_extiende(f, h):
	# Extiende listaHojas de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# 		 h, una hoja (lista de fórmulas como árboles)
	# Output: no tiene output, pues modifica la variable global listaHojas

	global listaHojas

	print("Formula:", Inorder(f))
	print("Hoja:", imprime_hoja(h))

	assert(f in h), "La formula no esta en la lista!"

	clase = clasificacion(f)
	print("Clasificada como:", clase)
	assert(clase != None), "Formula incorrecta " + imprime_hoja(h)

	if(clase=='1ALFA'):
		aux = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux += [f.right.right]
		listaHojas.append(aux)
	elif(clase=='2ALFA'):
		aux = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux += [f.left]+[f.right]
		listaHojas.append(aux)
	elif(clase=='3ALFA'):
		aux = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux += [complemento(f.right.left)] + [complemento(f.right.right)]
		listaHojas.append(aux)
	elif clase=='4ALFA':
		aux = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux += [f.left] + [complemento(f.right)]
		listaHojas.append(aux)
	#clasificacion y extencion formulas beta
	elif clase=='1BETA':
		aux = [x for x in h]
		aus = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aus.remove(f)
		aux += [complemento(f.right.left)]
		aus += [complemento(f.right.right)]
		listaHojas.append(aux)
		listaHojas.append(aus)
	elif clase=='2BETA':
		pass
	elif clase=='3BETA':
		pass


def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f

	global listaHojas
	global listaInterpsVerdaderas

	A = String2Tree(f)
	print(u'La fórmula introducida es:\n', Inorder(A))

	listaHojas = [[A]]

	while (len(listaHojas) > 0):
		h = choice(listaHojas)
		print("Trabajando con hoja:\n", imprime_hoja(h))
		x = no_literales(h)
		if x == None:
			if par_complementario(h):
				listaHojas.remove(h)
			else:
				listaInterpsVerdaderas.append(h)
				listaHojas.remove(h)
		else:
			clasifica_y_extiende(x, h)

	return listaInterpsVerdaderas


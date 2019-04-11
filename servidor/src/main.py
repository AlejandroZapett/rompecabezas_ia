from nodo import Nodo
from estructuras import Cola
from Tiempo import tiempo_ejecucion
import sys
import argparse

def rompecabezas(argumentos):

	@tiempo_ejecucion(argumentos)	
	class Main:
		
		def __init__(self, estado_inicial, estado_final):
			self.estado_final = estado_final
			self.estado_inicial = Nodo(estado_inicial)
			r = self.conseguir_ruta()

			#Para ejecutar el programa desde la interfaz grafica descomente estas líneas
			self.enviar_ruta(r)

			#Para ejecuta el programa desde la terminal descomente estas lineas
			self.imprimir_ruta(r)
			#==Segunda forma de obtener la ruta==
			self.imprimir_ruta_dos(r)
			#====================================



		def conseguir_ruta(self):
			#Definicion de condiciones iniciales 
			cola = Cola()
			estado_actual = self.estado_inicial
			visitados = []
			hijos = self.crear_hijos(estado_actual)

			#Algoritmo de busqueda BFS (por amplitud)
			while (self.es_solucion(estado_actual.conseguir_cadena()) == False):
				visitados.append(estado_actual.conseguir_cadena())
				hijos = self.crear_hijos(estado_actual)
				for x in hijos: 
					if x.conseguir_cadena() not in visitados:
						#==Segunda forma de obtener la ruta==
						x.establecer_ruta_al_nodo(estado_actual.ruta_al_nodo, estado_actual.conseguir_cadena()) #en cada nodo hijo guardo la ruta
						#====================================
						cola.push(x)
				estado_actual = cola.pop()
			visitados.append(estado_actual.conseguir_cadena()) #agrego el ultimo nodo al salir del while
			#==Segunda forma de obtener la ruta==
			estado_actual.establecer_ruta_al_nodo(estado_actual.ruta_al_nodo, estado_actual.conseguir_cadena())#guardo el ultimo nodo en la ruta
			#====================================
			return estado_actual

		def es_solucion(self, estado):
			if (estado == self.estado_final):
				return True
			else:
				return False


		def crear_hijos(self, nodo):
			cadena = nodo.conseguir_cadena()
			pos_vacia = cadena.find("0")
			positions = self.crear_posiciones(pos_vacia)
			return list(#convierto mapa a lista
				filter( #filtro aquellos que sean -1 --> ver funcion nueva_cadena, retorna -1
					lambda x: type(x) == Nodo,list(
						map(lambda x: self.nueva_cadena(nodo,pos_vacia,x),positions) #creo las nuevas cadenas
						)
					)
				)


		def crear_posiciones(self,pos_vacia):
			mod = (pos_vacia + 1) % 3 #me dice  si es una posicion en el extremo derecho o izquierdo
			if(mod == 0):
				return [pos_vacia - 3,
						pos_vacia - 1,
						pos_vacia + 3]
			elif (mod == 1):
				return [pos_vacia - 3,
						pos_vacia + 1,
						pos_vacia + 3]
			else:
				return [pos_vacia - 3,
						pos_vacia - 1,
						pos_vacia + 1,
						pos_vacia + 3]

		def conseguir_heuristica_1(self, estado_actual):
			index=0		
			estado_actual=nodo_actual.conseguir_cadena()
			estado_final= self.estado_final.conseguir_cadena()
			for idx, val in enumerate(estado_actual):#idx es posicion y val el valor de esa posicion
				if val != estado_final[idx]:
					index=index+1

			return index
			
		def conseguir_heuristica_2(self, estado_actual):
			distancia_manhatan = 0
			posiciones_estado_actual = estado_actual.conseguir_cadena();#obtenemos los valores del estado actual
			posiciones_originales = self.estado_final.conseguir_cadena();#obtenemos los valores del estado final
			for i,valor in enumerate(posiciones_estado_actual):#recorremos la lista de las posiciones del estado actual
															   #i: es el inidice, valor: es el valor segun el indice
				j = i-1#almacenamos el indice a un contador que almacenara
				distancia = 0
				bandera_encontrado = false#bandera que nos indicara si la posicion fue encontrada en la busqueda de izquierda a derecha
				while (j < 10):#buscamos el valor de izquierda a derecha, del 0 al 10
					if valor == posiciones_originales[j]:#preguntamos si el el valor esta en la posicion correcta
						distancia_manhatan += distancia   #si lo encuentra, entonces j lo sumamos a la distancia manhatan
						bandera_encontrado = true # e indicamos que ya se encontro el valor
						break
					else: #si no se encuentra, entonces aumentamos el contador, indicando que el valor esta desplazado
						j += 1
						distancia += 1
				if bandera_encontrado == false:#pregunta si el valor no se ha encontrado de izquierda derecha
					j -= 1 #le restamos 1 al indice indicadndo que empieze de 9  a 0
					distancia = 0
					while (j >= 0): #buscamos de derecha a izquierda
						if valor == posiciones_originales[j]:
							distancia_manhatan += distancia
							break
						else:
							j -= 1
							distancia += 1
			return distancia_manhatan #regresamos la distancia manhatan

		def nueva_cadena(self,nodo,posicion_cero,nueva_posicion):
			cadena = nodo.conseguir_cadena()
			if nueva_posicion >= 0 and nueva_posicion < 9: #evito tener error por un fuera de rango en el array
				nueva_cadena = cadena[:posicion_cero] + cadena[nueva_posicion] + cadena[posicion_cero + 1:]
				nueva_cadena = nueva_cadena[:nueva_posicion] + "0" + nueva_cadena[nueva_posicion + 1:]
				return Nodo(nueva_cadena.strip(),nodo)
			else:
				return -1 #los fuera de rango retornan esta bandera

		def imprimir_ruta(self,nodo_final): #imprime ruta de final a inicio, corregir esto
			nodo_actual = nodo_final
			while(nodo_actual != None):
				self.imprimir_como_matriz(nodo_actual.conseguir_cadena())
				nodo_actual = nodo_actual.conseguir_padre()

		#==Segunda forma de obtener la ruta==
		def imprimir_ruta_dos(self, nodo_final):
			ruta = nodo_final.conseguir_ruta_al_nodo()
			print("======== Ruta al nodo ========\n")
			for x in ruta:
				self.imprimir_como_matriz(x)
			print ("La ruta tiene "+str(len(nodo_final.ruta_al_nodo))+ " pasos")
		#====================================

		def imprimir_como_matriz(self,cadena):
			print(cadena[:3] + "\n" + cadena[3:6] + "\n" + cadena[6:] + "\n\n")

		def enviar_ruta(self, nodo_final):
			ruta = "" #"1,2,3,4,5,6,7,8,0 1,2,3,4,5,6,7,8,0 "
			for x in nodo_final.conseguir_ruta_al_nodo():
				for y in x:
					ruta = ruta+y+","
				ruta = ruta + " "
			ruta = ruta.replace(", ", " ")
			print(ruta)
	def leer_argumentos():
		parser = argparse.ArgumentParser(description='Definir tipo de heuristica')
		parser.add_argument('-t','--tipo_heuristica', required=True,help= 'Tipo de heuristica: h1 o h2')
		parser.add_argument('-a','--estados', required=True,help= 'Escribir estado inicial y estado final')

		args = parser.parse_args()
		argumentos= args.tipo_heuristica
		argumentos=[
			args.estados.split(" ")[0], 
			args.estados.split(" ")[1],
			args.tipo_heuristica

		]
		return argumentos

	if __name__ == '__main__':	
		#args = sys.argv[1].split(" ")
		#main = Main(args[0],args[1])
		#Entrada 
		argumentos = leer_argumentos()
		#Instancia
		rompecabezas(argumentos)
		


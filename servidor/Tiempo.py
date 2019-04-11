import time

def tiempo_ejecucion(message):
    def decorador(funcion):
        def wrapped():

            tiempo_inicio = time.time()

            funcion(message[0],message[1],message[2]) #3 argumentos 

            tiempo_final = time.time()

            print("Tiempo ejecucion: ", tiempo_final-tiempo_inicio)

            
        return wrapped
    return decorador

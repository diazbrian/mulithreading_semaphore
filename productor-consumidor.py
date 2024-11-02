import threading
import time
import random
from queue import Queue

# Tamaño del buffer compartido
BUFFER_SIZE = 5
buffer = Queue(BUFFER_SIZE)

# Semaforos para controlar el acceso al buffer
empty = threading.Semaphore(BUFFER_SIZE)  # Controla el espacio disponible (inicialmente igual al tamaño del buffer)
full = threading.Semaphore(0)  # Controla la cantidad de elementos en el buffer
mutex = threading.Lock()  # Exclusion mutua para acceso al buffer

def productor():
    while True:
        item = random.randint(1, 100)  # Genera un nymero aleatorio como "item"

        empty.acquire()  # Espera espacio disponible en el buffer
        mutex.acquire()  # Entra en la seccion critica

        # Agrega el item al buffer
        buffer.put(item)
        print(f"Productor produjo: {item}" + " Buffer: " + str(buffer.qsize()))

        mutex.release()  # Sale de la seccion critica
        full.release()  # Señala que hay un nuevo item en el buffer

        time.sleep(random.uniform(0.5, 2))  # Espera un poco antes de producir el siguiente

def consumidor():
    while True:
        full.acquire()  # Espera hasta que haya un item disponible en el buffer
        mutex.acquire()  # Entra en la seccion critica

        # Toma el item del buffer
        item = buffer.get()
        print(f"Consumidor consumio: {item}" + " Buffer: " + str(buffer.qsize()))

        mutex.release()  # Sale de la seccion critica
        empty.release()  # Señala que hay espacio disponible en el buffer

        time.sleep(random.uniform(0.5, 2))  # Espera un poco antes de consumir el siguiente


# Creacion de hilos para el productor y el consumidor
productor_thread = threading.Thread(target=productor)
consumidor_thread = threading.Thread(target=consumidor)

# Iniciar los hilos
productor_thread.start()
consumidor_thread.start()

# Esperar a que terminen (en este caso, corren indefinidamente)
productor_thread.join()
consumidor_thread.join()

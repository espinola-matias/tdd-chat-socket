import socket
import threading
import time
from servidor.servidor import ChatServer

# instanciamosel servidor y iniciamos poniendo en escucha con un time de 1s, crea el cliente y manda el nombre y recibe el mensaje de bienvenida del servidor, simula un time de 0,2s y cierra el socket
# crea hilo para cada mensaje y simula concurrencia y luego espera que los hilos finalicen y detiene el servidor de forma ordenada 
def test_multiples_clientes():
    servidor = ChatServer()
    servidor.start()
    time.sleep(0.5)

    mensajes_enviados = ["hola", "como estas", "todo bien", "adios"]
    clientes = []

    def cliente_func(mensaje):
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((servidor.host, servidor.port))
        cliente_socket.send(f"Cliente_{mensaje}".encode())
        cliente_socket.recv(1024)  
        cliente_socket.recv(1024)
        cliente_socket.send(mensaje.encode())
        time.sleep(0.2)
        cliente_socket.close()

    
    for mensaje in mensajes_enviados:
        hilo = threading.Thread(target=cliente_func, args=(mensaje,))
        clientes.append(hilo)
        hilo.start()

    for hilo in clientes:
        hilo.join()

    servidor.stop()
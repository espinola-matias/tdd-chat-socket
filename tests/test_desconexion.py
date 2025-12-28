import socket
import threading
import time
from servidor.servidor import ChatServer

# instancia el servidor, crea un hilo , activa y pone en escucha, da un time de 1 s y luego conecta un cliente simulado y manda el nombre y cierra abruptamente da un time 1s
# y cierra el servidor limpiando la lista de clientes 
def test_desconexion_repentina():
    servidor = ChatServer()
    thread = threading.Thread(target=servidor.start)
    thread.start()
    time.sleep(1)

    cliente1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente1.connect(("localhost", 9999))
    cliente1.send("Pepe".encode())
    cliente1.close()  

    time.sleep(1)
    servidor.stop()
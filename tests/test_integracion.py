import socket
import threading
import time
from servidor.servidor import ChatServer

# Arranca el servidor y damos un tiempo 
def test_verificar_chat_real():
    servidor = ChatServer(port=9999) 
    server_thread = threading.Thread(target=servidor.start)
    server_thread.start()
    time.sleep(1) 

    # lista de los mensajes recibidos 
    mensajes_recibidos = []

    def cliente_receptor():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 9999))
        sock.send("Lucas".encode())
        
        # Seteamos un timeout para que no se quede escuchando eternamente si algo falla
        sock.settimeout(3) 

        # Escuchamos mensajes del servidor
        try:
            while True:
                data = sock.recv(1024).decode()
                if not data: 
                    break
                mensajes_recibidos.append(data)
        except socket.timeout:
            pass 
        except Exception as e:
            print(f"Error en receptor: {e}")
        finally:
            sock.close()

    def cliente_emisor():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 9999))
        sock.send("Otto".encode())
        time.sleep(0.5)
        
        # Mensaje de prueba 
        sock.send("Hola Lucas, ¿me copias?".encode()) 
        time.sleep(0.5)
        sock.close()

    # iniciamos el hilo y damos tiempo 
    hilo_lucas = threading.Thread(target=cliente_receptor)
    hilo_lucas.start()
    time.sleep(0.5) 

    # Iniciamos el hilo del Emisor
    hilo_otto = threading.Thread(target=cliente_emisor)
    hilo_otto.start()

    # Esperamos a que el emisor termine
    hilo_otto.join()
    
    # detenemos el servidor 
    servidor.stop()
    hilo_lucas.join()
    server_thread.join()
    
    # Imprimimos lo que llego para depurar si falla
    print(f"\nMensajes recibidos: {mensajes_recibidos}")


    mensaje_esperado = "Hola Lucas, ¿me copias?"
    
    encontrado = False
    for mensaje in mensajes_recibidos:
        if mensaje_esperado in mensaje:
            encontrado = True
            break
    
    assert encontrado is True, f"El mensaje '{mensaje_esperado}' no fue recibido por Lucas"
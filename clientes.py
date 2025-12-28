import socket
import threading
import time

salir_cliente = False

# hilo de recibir mensajes en paralelo
def recibir_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024).decode()

            if mensaje == "El servidor a cerrado la conexion":
                print("El servidor finalizo las conexiones")
                break
            else:
                print(mensaje)
        except:
            if not salir_cliente:
                print("Error al recibir mensajes")
            break
    cliente.close()


def conectar_servidor():
    for intento in range(3):
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            cliente.connect(("localhost", 9999))
            return cliente
        except:
            print(f"No se pudo conectar, reintentando conexion intento {intento + 1} /3")
            time.sleep(1)
    else:
        print("No se logro restablecer la conexion con el servidor")
        exit()

def iniciar_cliente():
    global salir_cliente
    cliente = conectar_servidor()
    if not cliente:
        exit()

    while True:
        nombre = input("Ingresa tu nombre: ")
        if nombre:
            break
        print("Debes colocar tu nombre")

    cliente.send(nombre.encode())

    hilo = threading.Thread(target=recibir_mensajes, args=(cliente,)).start()
    
    while True:
        try:
            mensaje = input()
            if mensaje.strip().lower() == "salir":
                salir_cliente = True
                cliente.send(mensaje.encode())
                print("Haz abandonado el grupo")
                break
            else:
                cliente.send(mensaje.encode())
        except:
            print("Error al enviar mensaje, intentando reconectar")
            cliente.close()

            # nuevo intento de conexion
            cliente = conectar_servidor()
            if not cliente:
                exit()

            try:
                cliente.send(nombre.encode())
                print("Conexion restablecida")

                # nuevo hilo de escucha
                hilo = threading.Thread(target=recibir_mensajes, args=(cliente,))
                hilo.start()
            except:
                print("Fallo el reenvio de datos tras reconexion")
                break
    
    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()
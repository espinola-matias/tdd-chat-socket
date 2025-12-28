import socket
import threading

class ChatServer:
    # inicializar el objeto , haciendo referencia al socket del servidor, un flag que indica si el servidor esta activo usando un loop de aceptacion para detener, 
    # un mutex para sincronizar accesso a clientes activos evitando el dict simultaneo (runtimeEror) 
    def __init__(self, host="localhost", port=9999, max_conexiones=40):
        self.host = host
        self.port = port
        self.max_connections = max_conexiones
        self.clientes_activos = {}
        self.servidor_socket = None
        self.running = False
        self.lock = threading.Lock()

    # crea y arranca el socket con la bandera, si el porceso principal termina este hilono bloquea el del interprete 
    def start(self):
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind((self.host, self.port))
        self.servidor_socket.listen(self.max_connections)
        self.running = True
        print(f"Servidor iniciado en {self.host}:{self.port}")
        threading.Thread(target=self._aceptar_conexiones, daemon=True).start()

    # se acepta conexiones mientras la bander sea true
    def _aceptar_conexiones(self):
        while self.running:
            try:
                cliente, direccion = self.servidor_socket.accept()
                hilo = threading.Thread(target=self._manejar_cliente, args=(cliente, direccion), daemon=True)
                hilo.start()
            except OSError:
                break  

    # se maneja los clientes con el mutex para proteger, evitando modificaciones simultaneas 
    def _manejar_cliente(self, cliente, direccion):
        try:
            nombre = cliente.recv(1024).decode()
            with self.lock:
                self.clientes_activos[cliente] = nombre

            print(f"{nombre} se ha conectado desde {direccion}")
            self._broadcast(f"{nombre} se ha unido al chat", cliente)
            cliente.send("~ Para salir del chat escribe ('salir')\n".encode())
            cliente.send("~ Conectado al chat puedes iniciar una conversacion\n".encode())

            while True:
                mensaje = cliente.recv(1024).decode()

                if not ChatServer.validar_mensajes(mensaje):
                    cliente.send("Mensaje invalido (vacio o demasiado largo)\n".encode())
                    continue

                if mensaje.strip().lower() == "salir":
                    print(f"{nombre} se ha desconectado")
                    self._broadcast(f"{nombre} salio del chat", cliente)
                    break
                else:
                    self._broadcast(f"{nombre}: {mensaje}", cliente)
        except (ConnectionResetError, ConnectionAbortedError):
            print(f"Cliente {direccion} se a desconectado repentinamente")
        except Exception as e:
            print(f"Error con el cliente {direccion}: {e}")
        finally:
            cliente.close()
            with self.lock:
                if cliente in self.clientes_activos:
                    del self.clientes_activos[cliente]

    # funcion estatica que sirve para chequear que no vengan mensajes vacios o solo espacios y limita el tamaño de mensajes
    @staticmethod
    def validar_mensajes(mensaje):
        if not mensaje or not mensaje.strip():  
            return False
        if len(mensaje) > 256:  
            return False
        return True
    
    # funcion estatica si el mensaje esta vacio manda un texto indicativo y si esta todo correcto mandando los mensajes y quitando los espacios sobrantes 
    @staticmethod
    def formatear_mensaje(nombre, mensaje):
        if not mensaje or not mensaje.strip():
            return f"{nombre}: mensaje vacio"
        return f"{nombre}: {mensaje.strip()}"

    # reenvio de mensajes 
    def _broadcast(self, mensaje, cliente_emisor):
        with self.lock:
            for cliente in list(self.clientes_activos.keys()):
                if cliente != cliente_emisor:
                    try:
                        cliente.send(mensaje.encode())
                    except Exception:
                        cliente.close()
                        del self.clientes_activos[cliente]

    # cerrar conexion y limpiar clientes poniendo en falso la bandera de servidor activo
    def stop(self):
        self.running = False
        if self.servidor_socket:
            self.servidor_socket.close()
        with self.lock:
            for cliente in list(self.clientes_activos.keys()):
                try:
                    cliente.send("El servidor se ha cerrado.\n".encode())
                except Exception:
                    pass
                finally:
                    cliente.close()
            self.clientes_activos.clear()
        print("Servidor detenido correctamente")
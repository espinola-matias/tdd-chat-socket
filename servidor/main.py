from servidor import ChatServer

if __name__ == "__main__":
    servidor = ChatServer()
    servidor.start()

    try:
        while True:
            comando = input("Comando del servidor ('salir' para apagar): ")
            if comando.strip().lower() == "salir":
                servidor.stop()
                break
    except KeyboardInterrupt:
        servidor.stop()
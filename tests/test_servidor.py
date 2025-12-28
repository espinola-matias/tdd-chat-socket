from servidor.servidor import ChatServer

# pruebas unitarias usando los metodos estaticos TDD se prueban todos los casos y luego se implementa las funciones 
def test_valid_message():
    assert ChatServer.validar_mensajes("Hola mundo") is True

def test_empty_message():
    assert ChatServer.validar_mensajes("") is False

def test_whitespace_message():
    assert ChatServer.validar_mensajes("   ") is False

def test_long_message():
    assert ChatServer.validar_mensajes("x" * 300) is False

def test_max_length_message():
    assert ChatServer.validar_mensajes("x" * 256) is True

def test_formatear_mensaje():
    mensaje = ChatServer.formatear_mensaje("Pepe", "Mundo")
    assert mensaje == "Pepe: Mundo"
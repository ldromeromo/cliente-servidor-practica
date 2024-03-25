''' 
    Cliente de Chat
    ---------------
    Autor: Laura Daniela Romero Montañez

    Descripción:
    Este script implementa el lado cliente de una aplicación de chat que se comunica con un servidor a través de una red 
    local usando el protocolo TCP/IP. Permite a los usuarios conectarse a un servidor especificando su dirección IP y puerto 
    (ej. http://localhost, http://127.0.0.1, http://ip_del_equipo:puerto). Una vez conectados, los clientes pueden enviar preguntas o 
    mensajes al servidor y recibir respuestas. El servidor debe estar ejecutándose y escuchando en la dirección y puerto especificados 
    para que la conexión tenga éxito. Los clientes pueden desconectarse en cualquier momento usando una opción de terminación específica.

    Funcionalidades:
    - Conexión a un servidor chat mediante TCP/IP.
    - Envío de mensajes al servidor y recepción de respuestas.
    - Desconexión segura del chat.
    
    Métodos:
    - obtener_datos_servidor: Solicita al usuario la dirección IP y el puerto del servidor.
    - crear_socket: Crea un nuevo socket TCP/IP para la comunicación.
    - conectarse: Establece la conexión con el servidor usando el socket creado.
    - intento_conexion: Realiza hasta tres intentos para conectarse al servidor.
    - recibir: Espera y recibe mensajes del servidor.
    - main: Función principal que orquesta el flujo del programa.
'''

# Importar dependecias
from socket import *
import time

# Usar funciones
"""
Solicita al usuario la dirección IP y el puerto del servidor al que desea conectarse.
Retorna una tupla con la dirección IP y el puerto como enteros.
"""
def obtener_datos_servidor():
    try:
        host = input("Dirección del servidor: ") # Ejemplo: 127.0.0.1
        port = int(input("Puerto: ")) # Ejemplo: 7777
        return host, port
    except Exception as e:
        print("Error " + str(e))
        return e
        
"""
Crea y configura un socket TCP/IP no bloqueante con un tiempo de espera largo.
Retorna el socket configurado o None en caso de error.
"""
def crear_socket():
    try:
        # socket.AF_INET es el dominio del conector, En este caso, un conector IPv4.
        # socket.SOCK_STREAM tipo del conector, dependiente del parámetro anterior.
        s = socket(AF_INET, SOCK_STREAM)
        s.setblocking(False) # Proceso no bloqueante.
        s.settimeout(600000) # Tiempo de espera en milisegundos.
        return s
        
    except Exception as e:
        print("Error " + str(e))
    
"""
Intenta establecer una conexión con el servidor especificado por host y port utilizando el socket s.
Retorna True si la conexión es exitosa, False en caso contrario.
""" 
def conectarse(host, port, s):
    try:
        s.connect((host, port))
        print(f"Conexión establecita con el servidor en: {host}:{port}")
        return True
    except Exception as e:
        print("Error de conexión", str(e))
        return False

"""
Realiza hasta tres intentos para conectar con el servidor, esperando 5 segundos entre cada intento.
Retorna True si la conexión es exitosa, False si falla después de tres intentos.
"""   
def intento_conexion(host, port, s):
    try:
        intentos = 0
        while intentos < 3 : # Intenta conectar 3 veces
            if conectarse(host, port, s):
                return True
            intentos += 1
            print("Intentos de conexión número: ", intentos)
            time.sleep(5)
        print("No se pudo estableces la coneción con el servidor después de 3 intentos ")
        return False
    except Exception as e:
        print("Error " + str(e))
        
"""
Espera y recibe un mensaje del servidor a través del socket s.
Retorna el mensaje recibido decodificado.
"""
def recibir(s):
    try:
        strResp = s.recv(2048)
        strResp = strResp.decode("utf-8") # 8-bit Unicode Transport Format
        return strResp
        
    except Exception as e:
        print("Error " + str(e))
 
"""
Función principal del cliente. Solicita la dirección y puerto del servidor, intenta establecer una conexión,
y permite al usuario enviar y recibir mensajes hasta que decida terminar la sesión enviando "terminar".
"""       
def main():
    try:
        host, port = obtener_datos_servidor()
        if host and port:
            s = crear_socket()
            if intento_conexion(host, port, s):
                print(recibir(s))
                while True:
                    strMsg = input("Mensaje: ")
                    s.send(strMsg.encode("utf-8"))
                    strResp = recibir(s)
                    if strResp.lower() == "terminar": # Si se escribe "terminar" finaliza la conexión.
                        break
                    print(f"Servidor contesta: {strResp}")
                    
            else:
                print("No se pudo estableces la conexión con el servidor")
                s.close
    except Exception as e:
        print("Error " + str(e))
        
if __name__ == "__main__":
    main()
        

        
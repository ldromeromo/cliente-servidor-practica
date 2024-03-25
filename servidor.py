''' 
Servidor de Chat
----------------
Autor: Laura Daniela Romero Montañez

Descripción:
Este script implementa el lado servidor de una aplicación de chat, funcionando sobre una red local mediante el protocolo TCP/IP. Está diseñado para escuchar conexiones entrantes de clientes, procesar sus mensajes y enviar respuestas adecuadas. Los clientes pueden preguntar al servidor y recibir asistencia, por ejemplo, con problemas matemáticos simples. El servidor permanece activo indefinidamente, esperando por clientes, hasta que se detiene manualmente. Soporta múltiples conexiones de clientes de manera concurrente, gestionando cada una en un hilo separado para una comunicación eficiente.

Funcionalidades:
- Escucha y acepta conexiones de clientes a través de TCP/IP.
- Procesamiento y respuesta a mensajes de clientes.
- Soporte para múltiples clientes de manera concurrente.
- Capacidad de realizar operaciones matemáticas simples a petición del cliente.   

Métodos:
- ini: Inicializa el servidor solicitando la dirección IP y el puerto.
- crear_socket: Configura un nuevo socket TCP/IP.
- ligar_Socket: Asocia el socket a una dirección IP y puerto específicos.
- conexiones: Escucha y acepta conexiones entrantes de clientes.
- saludo: Envía un mensaje de bienvenida a los clientes recién conectados.
- realizar_operacion: Calcula la resolución de los problemas matemáticos.
- responder: Procesa y responde a los mensajes recibidos de los clientes.
- manejo_Cliente: Gestiona la comunicación con cada cliente conectado.
- main: Función principal que orquesta el flujo del programa.
'''

# Llamaremos las librerias de python
from socket import socket, AF_INET, SOCK_STREAM, error
from _thread  import * # Para lanzar un hilo (<<thread>>) en python via el módulo estandar <<threading>>
import time
import threading # La técnica que permite que una aplicación ejecute simultaneamente simuntáneamente varios operaciones en el ...
import sys # Sys - parametros y funciones especificos del sistema
import re

listaClientes = list() # Escuchamos hasta n clientes
# Aquí creamos las funciones enunciadas en los comentario y como se desarrollan
# Definamos las dirección I´de este servidor  SERVER_ADDRESS = '127.0.0.1' # Definamos el puerto de escucha SERVER_PORT = 2222

def ini():
    try:
        host = input("Servidor: ")
        port = int(input("Puerto: "))
        return host, port
    
    except Exception as e:
        print("Error " + str(e))
        exit()

def crear_socket():
    try:
        # socket.SOCK_STREAM tipo del conector, dependiento el parametro anterior (no todos los dominios)...
        s = socket(AF_INET, SOCK_STREAM)
        
        # ahora conectése al servidor web en el puerto 80: el puerto http normal.
        # usa socket.setblocking(False) para que no sea bloqueante
        s.setblocking(False)
        # establece un temporizador que ejecuta una función a una pieza de código especifico una vez que ...
        s.settimeout(600000)
        return s
    
    except Exception as e:
        print("Error " + str(e))
    
def ligar_Socket(host, port, s): # (host, port) para la familia de direciones AF_INET, donde host es una cadena que representa un...
    while True:
        try:
            s.bind((host, port)) # Define IP and Port # Asociamos el socket con la dirección IP y el Puerto
            break
        except error as e:
            print("Error ", str(e))

# Listo, ahora comenzamos a escuchar y capturar los datos que nos envien los clientes
def conexiones(s):
    try:
        conn, addr = s.accept()
        print(f"\nConexión establecida \nel cliente es: {addr[0]} : {addr[1]} \n")
        return conn, addr
    
    except Exception as e:
        print("Error " + str(e))
    
def saludo(conn):
    try:
        strMensaje = "\nBienvenido, estas conectado al servidor!!! \nSi tienes un problema matemático simple estare encantado de responderlo. "
        conn.send(strMensaje.encode("utf-8"))
    except Exception as e:
        print("Error " + str(e))
        
def realizar_operacion(match):
    operacion_sin_espacios = re.sub(r'\s*', '', match)
    # Identificamos los números y el operador
    numeros = re.split(r'[\+\-\*/]', operacion_sin_espacios)
    operador = re.search(r'[\+\-\*/]', operacion_sin_espacios).group()
    
    if "+" in operador:
        return str(float(numeros[0]) + float(numeros[1]))
    elif "-" in operador:
        return str(float(numeros[0]) - float(numeros[1]))
    elif "*" in operador:
        return str(float(numeros[0]) * float(numeros[1]))
    elif "/" in operador:
        return str(float(numeros[0]) / float(numeros[1]))
    
def responder(conn, strMsgIn): # Recibimos informacón del cliente. Usamos el método strMsgIn[::-1]para cifrar el mensaje
    try:
        # strMensaje = "Mensaje - " + strMsgIn[::-1]
        saludos = ["hola", "buenos días", "buenas"]
        if any(saludo in strMsgIn.lower() for saludo in saludos):
            strMensaje = "Hola, ¿tienes algún problema matemático?"
        else:
            # Buscamos operaciones matemáticas en el mensaje            
            operacion = re.search(r'\d+\s*[\+\-\*/]\s*\d+', strMsgIn)
            if operacion:
                resultado = realizar_operacion(operacion.group(0))
                strMensaje = f"El resultado es {resultado}."
            else:
                # Si no se encuentra una operación matemática válida, solicitamos un problema matemático
                strMensaje = "Por favor, dame un problema matemático para resolver."
                
        conn.send(strMensaje.encode("utf-8"))

    except Exception as e:
        print("Error " + str(e))
        
def manejo_Cliente(conn, addr): # Recibimos informacón del cliente. Usamos el método strMsgIn[::-1]para cifrar el mensaje
    try:
        while True: #While connection is true
            strReq = conn.recv(2048)
            strReq = strReq.decode("utf-8") # Recibimos información del cliente. Usamos el método decode() porque la información viene...
            if strReq.lower() == "terminar": # Si el cliente escribe "Terminar" finaliza la conexión.
                conn.send("terminar".encode("utf-8"))
                print("Conexión finalizada por el cliente")
            print(f"Cliente envia: {strReq}: código de cliente: {addr[1]} \n")
            responder(conn, strReq)

    except Exception as e:
        print("Error para cliente: " + str(e))
    finally:
        conn.close()
        print(f"Conexión con el cliente ({addr[0]}:{addr[1]}) cerrada")
        
# Aquí vamos a crear nuestra función principal o Main
def main():
    try:
        bandera = True
        host, port = ini()
        s = crear_socket()
        ligar_Socket(host, port, s)
        s.listen()
        print("\nAdvertancia: este servidor es de tipo Esclavo, no, escribe si el servidor no tiene ningún mensaje para responder a los clientes")
        print(f"Escuchando es {host}:{port} ")
        print("Esperamos por los clientes ")
        while True: # Este código es importante para que los hilos no se rompan
            conn, addr = conexiones(s)
            # Esta variable espero a los clientes
            if addr not in listaClientes:
                saludo(conn)
                listaClientes.append(addr)
                print("\nCliente conectado!!!")
            thread = threading.Thread(target = manejo_Cliente, args =(conn, addr,))
            thread.start()
            
    
    except Exception as e:
        print("Error " + str(e))
    finally:
        conn.close()
         
if __name__ == "__main__":
    main()


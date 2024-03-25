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

# Importar dependecias
from socket import socket, AF_INET, SOCK_STREAM, error
from _thread  import * # Para lanzar un hilo (<<thread>>) en python via el módulo estandar <<threading>>
import time
import threading # La técnica que permite que una aplicación ejecute simultaneamente simuntáneamente varios operaciones en el ...
import sys # Sys - parametros y funciones especificos del sistema
import re

listaClientes = list() # Se guarda hasta n clientes

"""
Solicita al usuario ingresar la dirección IP y el puerto donde el servidor estará escuchando.
Retorna la dirección IP y el puerto como una tupla.
"""
def ini():
    try:
        host = input("Servidor: ")
        port = int(input("Puerto: "))
        return host, port    
    except Exception as e:
        print("Error " + str(e))
        exit()

"""
Crea un socket TCP/IP configurado para ser no bloqueante y con un largo tiempo de espera.
Retorna el socket configurado.
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
Vincula el socket s a la dirección IP y puerto especificados. Reintenta en caso de error.
No retorna ningún valor.
"""
def ligar_Socket(host, port, s):
    while True:
        try:
            s.bind((host, port)) # Define IP and Port # Asociamos el socket con la dirección IP y el Puerto
            break
        except error as e:
            print("Error ", str(e))

"""
Espera y acepta una conexión entrante. Imprime la dirección y puerto del cliente conectado.
Retorna el objeto de conexión y la dirección del cliente.
"""
def conexiones(s):
    try:
        conn, addr = s.accept()
        print(f"\nConexión establecida \nel cliente es: {addr[0]} : {addr[1]} \n")
        return conn, addr
    
    except Exception as e:
        print("Error " + str(e))
    
"""
Envía un mensaje de bienvenida al cliente recién conectado.
"""
def saludo(conn):
    try:
        strMensaje = "\nBienvenido, estas conectado al servidor!!! \nSi tienes un problema matemático simple estare encantado de responderlo. "
        conn.send(strMensaje.encode("utf-8"))
    except Exception as e:
        print("Error " + str(e))
        
"""
Realiza una operación matemática simple basada en la expresión encontrada en el mensaje del cliente.
Retorna el resultado de la operación como una cadena.
"""
def realizar_operacion(match):
    operacion_sin_espacios = re.sub(r'\s*', '', match)
    # Identificamos los números y el operador para realizar la operación
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
    
"""
Procesa y responde a los mensajes recibidos del cliente.
Si el mensaje contiene una operación matemática válida, calcula y envía el resultado.
De lo contrario, solicita al cliente que proporcione un problema matemático.
"""
def responder(conn, strMsgIn):
    try:
        saludos = ["hola", "buenos días", "buenas"]
        if any(saludo in strMsgIn.lower() for saludo in saludos):
            strMensaje = "Hola, ¿tienes algún problema matemático?"
        else:
            # Se identifica operaciones matemáticas en el mensaje            
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
        
"""
Gestiona la comunicación con un cliente conectado. Recibe mensajes del cliente, responde a estos mensajes,
y finaliza la conexión si el cliente envía "terminar".
"""
def manejo_Cliente(conn, addr):
    try:
        while True: #While si la conexión es true
            strReq = conn.recv(2048)
            strReq = strReq.decode("utf-8") # Recibimos información del cliente. Usamos el método decode() para decodificar información.
            if strReq.lower() == "terminar": # Si el cliente escribe "terminar" finaliza la conexión.
                conn.send("terminar".encode("utf-8"))
                print("Conexión finalizada por el cliente")
            print(f"Cliente envia: {strReq}: código de cliente: {addr[1]} \n")
            responder(conn, strReq)

    except Exception as e:
        print("Error para cliente: " + str(e))
    finally:
        conn.close()
        print(f"Conexión con el cliente ({addr[0]}:{addr[1]}) cerrada")
        
"""
Función principal del servidor. Inicializa el servidor solicitando la dirección IP y el puerto para escuchar.
Crea y vincula el socket a la dirección y puerto especificados. Comienza a escuchar conexiones entrantes.
Para cada conexión entrante, envía un saludo y crea un nuevo hilo para manejar la comunicación con ese cliente.
Continúa aceptando nuevos clientes y mantiene la comunicación hasta que se interrumpe manualmente.
"""
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
        while True: #While si la conexión es true. Este código es importante para que los hilos no se rompan
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


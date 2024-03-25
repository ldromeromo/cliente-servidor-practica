''' SERVIDOR
Programa servdiros para la construcción de un chat
Creado por: Laura Daniela Romero Montañez
De que se trata el código:
    El presente código es para crear un servidor chat que corre a través de una red local mediante el protocolo TCP/IP a través de unos permisos de IP
    Ejem: http://localhost; http://127.0.0.1; http://ip_del_equipo puerto 2323
    
    El servidor hace las veces de conectar a clientes y ellos le preguntan al servidor a través del chat 
    que puedes hacer y que necesitan del servidor. Esto provoca los clientes abren la conexió, el servidor
    en este ejercicio el actua como esclavo de los clientes hasta que los clientes le hablen el no puede
    constestar. El servidor se mantiene ejecutandose siempre hasta que desde la linea de comandos lo saquemos, esto nos lleva
    que el servidor espere a los clientes por siempre, Los clientes se pueden salir mediantes la opción "terminar" ctr + z, estos avisan al...
    si un cliente se ha salido. Los clientes le escriben al servidor y se comunicas en orden de llegada si dos mensajes llegan
    de diferente cliente el servidor respondera cada mensaje en el orden que llegan.
Funciones que se van a usar:
    ini(), esta pide al usuario la IP del host del servidor y el puerti necesario en el sockets
    crear_socket(), este nos retorna un nuevo sockes siguiendo el esquema del protocolo TCP
    ligar_Sockers(Host, Port), une un socket a los datos que se dan para el host y el port
    conexiones(), esta espera por la coneció de un cliente y nos devuelve la ip del cliente y el puerto del cliente.
    responder(conn), maneja los mensajes revibidos de cada cliente. La función enviar es llamada una vez que recibe un mensaje
    manejo_Cliente(conn), en esta el servidor la adjudica un número a un cliente y le envía un mensaje...
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


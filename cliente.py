''' CLIENTE
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
from socket import *
import time

# Usar funciones
def obtener_datos_servidor():
    try:
        host = input("Dirección del servidor: ") # 127.0.0.1
        port = int(input("Puerto: ")) # 7777
        return host, port
    except Exception as e:
        print("Error " + str(e))
        return e
        
def crear_socket():
    try:
        # Función para crear un socket, un conector para poder realizar conexiones de red.
        # socket.AF_INET es el dominio del conector, En este caso, un conector IPv4.
        # socket.SOCK_STREAM tipo del conector, dependiente del parámetro anterior.
        s = socket(AF_INET, SOCK_STREAM)
        s.setblocking(False)
        s.settimeout(600000)
        return s
        
    except Exception as e:
        print("Error " + str(e))
    
def conectarse(host, port, s):
    try:
        s.connect((host, port))
        print(f"Conexión establecita con el servidor en: {host}:{port}")
        return True
    except Exception as e:
        print("Error de conexión", str(e))
        return False
    
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
        
def recibir(s):
    try:
        strResp = s.recv(2048)
        strResp = strResp.decode("utf-8") # 8-bit Unicode Transport Format
        return strResp
        
    except Exception as e:
        print("Error " + str(e))
        
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
                    # s.send(strMsg.encode("utf-8")[2048])
                    strResp = recibir(s)
                    if strResp.lower() == "terminar":
                        break
                    print(f"Servidor contesta: {strResp}")
                    
            else:
                print("No se pudo estableces la conexión con el servidor")
                s.close
    except Exception as e:
        print("Error " + str(e))
        
if __name__ == "__main__":
    main()
        

        
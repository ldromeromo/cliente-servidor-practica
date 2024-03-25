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

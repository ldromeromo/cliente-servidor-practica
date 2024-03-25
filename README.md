# Aplicación de Chat TCP/IP

## Autor
Laura Daniela Romero Montañez

## Descripción
Esta aplicación de chat permite la comunicación entre un servidor y múltiples clientes a través de una red local usando el protocolo TCP/IP. Está compuesta por dos scripts principales: uno para el servidor y otro para el cliente. Los usuarios pueden conectarse al servidor usando la dirección IP y puerto adecuados, enviar mensajes, y recibir respuestas. El servidor puede manejar solicitudes de múltiples clientes concurrentemente, respondiendo a cada uno según el orden de llegada de los mensajes.

## Funcionalidades
- **Cliente:**
  - Conexión a un servidor mediante TCP/IP.
  - Envío y recepción de mensajes.
  - Desconexión segura del chat.
- **Servidor:**
  - Escucha de conexiones entrantes a través de TCP/IP.
  - Gestión de múltiples clientes de manera concurrente.
  - Procesamiento y respuesta a mensajes de clientes.
  - Ejecución de operaciones matemáticas simples por solicitud del cliente.

## Cómo Usar
1. **Iniciar el Servidor:**
   - Ejecutar el script del servidor.
   - Ingresar la dirección IP y puerto donde el servidor escuchará conexiones.
2. **Conectar con el Cliente:**
   - Ejecutar el script del cliente en una máquina diferente o en la misma máquina pero en una terminal distinta.
   - Ingresar la dirección IP y puerto del servidor al que se desea conectar.
3. **Comunicación:**
   - Una vez establecida la conexión, los clientes pueden comenzar a enviar mensajes al servidor.
   - Para desconectarse, el cliente debe enviar una señal de terminación específica (por ejemplo, "terminar").

## Requisitos
- Python 3


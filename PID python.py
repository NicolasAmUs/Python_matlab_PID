import socket
import struct
import time

#constantes para un zita de 0.7 y un ts=10s
kp = 1.2
ki = 2
kd = 0.1
T = 0.1  #tiempo de muestreo (coincide con el tiempo de muestreo de matlab)     

error_previo = 0
integral = 0

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket a una dirección y puerto
server_address = ('localhost', 8000)
server_socket.bind(server_address)

# Escuchar por conexiones entrantes
server_socket.listen(1)
print('Servidor socket escuchando en el puerto 8000...')

# Aceptar la conexión entrante
client_socket, client_address = server_socket.accept()
print(f'Cliente conectado desde {client_address}')
Control=0
while True:
    datos_recibidos = client_socket.recv(1024)
    plant_input = struct.unpack('>f', datos_recibidos[-4:])[0] #> porque es big endian
    if not datos_recibidos:
        print('No hay datos recibidos del cliente. Desconectando...')
    error = plant_input  # Datos recibidos corresponden al error entre entrada y retroalimentacion
    integral += error * T #Calculo parte integral 
    derivada = (error - error_previo) / T #Calculo error derivativo
    Control = kp * error + ki* integral + kd*derivada #PID
    numero_codificado = struct.pack('!f', Control) # Envio de datos En formato big endian
    client_socket.sendall(numero_codificado)
    time.sleep(0.01)  # Retardo de 0.01 segundos


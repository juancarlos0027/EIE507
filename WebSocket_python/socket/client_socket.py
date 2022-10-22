import socket
import uuid

HEADER = 64
PORT = 8080
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.1.20'
#SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

autorizacion = False

def getMacAddress():
    mac = hex(uuid.getnode()).replace('0x', '').upper()
    #Cambia el formato de la mac address para que sea mas legible
    mac = ':'.join(mac[i: i + 2] for i in range(0, 11, 2))
    return mac

def send(msg):
    global autorizacion
    message = msg.encode(FORMAT) #encode the message in byte format o encode str in byte object
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)#encode the lenght of the message
    send_length += b' ' * (HEADER - len(send_length))# darle el largo al mensaje de 64
    #b'' byte representación
    client.send(send_length)
    client.send(message)

    if(autorizacion == False):
        if(str(client.recv(2048).decode(FORMAT)) == "handshake|OK"):
            autorizacion = True
            print("Conexion exitosa")
        elif(str(client.recv(2048).decode(FORMAT)) == "handshake|FAIL"):
            autorizacion = False
            print("Handshake fallido")
        else:
            autorizacion = False
            print("Error en handshake")
    else:
        print(client.recv(2048).decode(FORMAT))

print("MAC: " + getMacAddress()+"\n")

# Se envía el mensaje indicando que se está realizando el handshake
send("handshake|"+getMacAddress())

if(autorizacion == True):
    print("Ahora puedes enviar mensajes")
else:
    print("No se pudo conectar por lo que no puedes enviar mensajes")

""" Casos_activos = 123
muertes = 123
msg = "Casos_activos," + str(Casos_activos)+ ", muertes," + str(123)
send(msg)

test_data = list()
test_data = [12, 12]
data_socket = 'temperature='+str(test_data[0])+','+'Humidity='+str(test_data[1])
send(data_socket)
input()
send("Hello Everyone!")
input()
send("Hello EIE!") """

print("Escriba CERRAR para cerrar la conexión")
# entra en un bucle para enviar mensajes y verificar si se debe cerrar la conexión
while True:
    msg = input("Escriba un mensaje: ")
    if(msg == "CERRAR"):
        send(DISCONNECT_MESSAGE)
        break
    else:
        send(msg)
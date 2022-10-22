import socket
import threading

HEADER = 64
PORT = 8080
SERVER = '192.168.1.20'
#socket.gethostbyname(socket.gethostname())
#osip = os.popen('curl ifconfig.me').readline()
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
#####
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #make new socket, primir argumento la familia de socket que posemos escojer
#AF_INET que tipo de ip o que tipo de address----y el segundo argumento simplemente es estandar donde le decimo que queremos un socket
#para stream
server.bind(ADDR)#ADDR necesariemente necesita ser un tuple.

# lista de macs autorizadas
macs = [
    "A4:2B:8C:1D:2E:3F",
    "B5:3C:9D:2E:4F:5G",
    "C6:4D:0E:3F:5G:6H",
    "D7:5E:1F:4G:6H:7I"
    "94:08:53:5A:F9:1A",
]

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    # flag para saber si se ha realizado el handshake
    autorizacion = False

    connected = True
    #cuando estemso conectados
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)#HEDEAR how many bytes we recive
        if msg_length:#if the message has some content
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            #separar datos

            if msg == DISCONNECT_MESSAGE:
                connected = False

            #Se busca por el caracter | para separar los datos recibidos y buscar las instrucciones y sus parámetros
            if msg.split("|")[0] == "handshake":
                print("Realizando handshake")

                #Se busca la mac en la lista de macs autorizadas
                if msg.split("|")[1] in macs:
                    conn.send("handshake|OK".encode(FORMAT))
                    print("Conexion exitosa")
                    autorizacion = True
                else:
                    #Si la mac no está en la lista de macs autorizadas se envía un mensaje de error
                    conn.send("handshake|FAIL".encode(FORMAT))
                    print("Conexion fallida")
                    autorizacion = False

            # Solo se realizan acciones una vez se ha realizado el handshake
            if autorizacion:
                print(f"[{addr}] {msg}")
                conn.send("Mensaje recibido".encode(FORMAT))

    conn.close()

def start():
    try:
        server.listen()
        print(f"[LISTENING] Server is listening on address {ADDR}")
        while True:
            conn, addr = server.accept()#espera aca hasta que ocurra una nueva conexión donde guarda el objeto socket y el address el cual nos permite
            #                               comunicaros hace el cliente
            #ahora declaramos un threath para manejar la conección de ese cliente
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            #imprimir cuantas conexiónes activas tenemos
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    except:
        print("Error en el servidor")
        server.close()

print("[STARTING] server is starting...")
start()

cursor.commit()

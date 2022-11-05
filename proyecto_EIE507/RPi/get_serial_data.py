#!/usr/env/bin python3
# Programa principal para lectura de datos en el puerto serial de la Raspberry Pi

import serial
import time
import datetime

# Configuramos el puerto serial interno de la Raspberry Pi
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# Entramos en un bucle infinito para leer los datos del puerto serial
while True:
    # Leemos los datos del puerto serial
    data = ser.readline()
    # Si los datos no son nulos, los imprimimos en pantalla
    if data:
        # Separa los datos por dos puntos
        data = data.decode('utf-8').split(':')
        
        # Imprime los datos del sensor de CO
        print('ID: ' + data[0])
        print('CO: ' + data[1] + ' ppm')

        # Imprime la fecha y hora
        print(datetime.datetime.now())



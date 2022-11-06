#!/usr/env python3
# Programa principal para lectura de datos en el puerto serial de la Raspberry Pi

import serial
import time
import datetime

# Configuramos el puerto serial interno de la Raspberry Pi
ser = serial.Serial('/dev/ttyS0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)

# Entramos en un bucle infinito para leer los datos del puerto serial
while True:
    try:
        # Leemos los datos del puerto serial
        data = ser.readline()
        # Si los datos no son nulos, los imprimimos en pantalla
        if data:
            # Separa los datos por dos puntos
            
            data = data.decode('utf8')
            print(data)
            """ data = data.split(':')
            
            # Imprime los datos del sensor de CO
            print('ID: ' + data[0])
            print('CO: ' + float(data[1]) + ' ppm') """

            # Imprime la fecha y hora
            print(datetime.datetime.now())
            

    except KeyboardInterrupt:
        print('\nAdquisicion finalizada\n')
        break

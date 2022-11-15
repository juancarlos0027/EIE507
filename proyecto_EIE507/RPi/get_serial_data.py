#!/usr/env python3
# Programa principal para lectura de datos en el puerto serial de la Raspberry Pi

import serial
import time
import datetime

# Configuramos el puerto serial interno de la Raspberry Pi
ser = serial.Serial('/dev/ttyAMA0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)

# Entramos en un bucle infinito para leer los datos del puerto serial
while True:
    try:
        # Leemos los datos del puerto serial provenientes del ESP8266
        data = ser.readline()

        if(len(data) > 0):
            # Imprimimos los datos en la consola
            try:
                model, value = data.decode('utf-8').split(':')
                value = float(value)
                print(f'{model}: {value} PPM - {datetime.datetime.now()}')

            except:
                print('[ Error en la lectura de datos ]')
                continue

    except KeyboardInterrupt:
        print('\nAdquisicion finalizada\n')
        break

#!/usr/bin/env python3
""" Programa principal corriendo en raspberry pi.
Se conecta al puerto serial del USB, que a su vez se conecta al arduino.
Y lee los valores del puerto serial. 

Autores: Juan Carlos Muñoz
         José Henríquez
"""

import serial
import time

def map(x, in_min, in_max, out_min, out_max):
    """ Función que mapea un valor de un rango a otro. """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def procesarDatoSensor(data):
    # separa los datos
    data = data.split(':')
    # convierte a int data[1]
    data = int(data[1])
    # mapea los valores para 0 a 100°C
    data = map(data, 0, 1023, 0, 100)
    # retorna el valor de la temperatura en °C
    return data

def main():
    """ Función principal. """
    # Se abre el puerto serial especificado en la ruta, a 9600 baudios.
    print("** Conectando a puerto serial...", end = '')
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
    except Exception as e:
        print("** Error al conectar a puerto serial.")

    try:
        print("** Conectado. Esperando datos...")
        while True:
            data = ser.readline().decode('utf-8').strip()
            #Si data comienza con 'val:' son los datos de los sensores
            # verifica si el dato es de los sensores
            if data.startswith('val:'):
                temperatura = procesarDatoSensor(data)
                print('Temperatura: {}°C'.format(temperatura))
            else:
                print(data)    
    except Exception as e:
        print("** Se ha perdido la conexión con el puerto serial")

if __name__ == '__main__':
    while True:
        main()
        time.sleep(1)
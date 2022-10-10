#!/usr/bin/env python3
""" Programa principal corriendo en raspberry pi.
Se conecta al bus I2C de los GPIO y lee los datos del sensor de dirección 8.

Autores: Juan Carlos Muñoz
         José Henríquez
"""

import sys
import smbus2 as smbus
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

def convertirStringABye(inputString):
  convertido = []
  for b in inputString:
    # Convierte el caracter a su valor en la tabla ASCII (decimal)
    convertido.append(ord(b))
  return convertido

def main():
    """ Función principal. """
    
    # Slave Addresse
    I2C_SLAVE_ADDRESS = 8 #0x08 dirección del arduino en el bus I2C

    # Se abre el bus i2c de la raspberry
    I2Cbus = smbus.SMBus(1)

    with smbus.SMBus(1) as I2Cbus:
        BytesToSend = convertirStringABye(":T") # envía :T para pedir la temperatura
        I2Cbus.write_i2c_block_data(I2C_SLAVE_ADDRESS, 0, BytesToSend)
        time.sleep(0.1)

        # lee los datos del sensor
        while True:
            try:
                data = I2Cbus.read_i2c_block_data(I2C_SLAVE_ADDRESS,0x00,16)
                print("Recibido desde Arduino:")
                print(data)
                # convierte los datos y los procesa
                data = procesarDatoSensor(str(data))
            except:
                print("Error de lectura")
                time.sleep(0.5)
   
if __name__ == '__main__':
    while True:
        # ejecuta la función principal cada 1 segundo
        main()
        time.sleep(1)
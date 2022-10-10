#!/usr/bin/env python3
""" Programa principal corriendo en raspberry pi.
Se conecta al bus I2C de los GPIO y lee los datos del sensor de dirección 8.
Además considera la clase Sensor para leer los datos del sensor de temperatura.
keywords: i2c, sensor, temperatura, getter, setter, clase, python

Autores: Juan Carlos Muñoz
         José Henríquez
"""

import sys
import smbus2 as smbus
import time

class Sensor:
    """ Clase que representa un sensor. """
    def __init__(self, I2Cbus, I2C_SLAVE_ADDRESS):
        self.I2Cbus = I2Cbus
        self.I2C_SLAVE_ADDRESS = I2C_SLAVE_ADDRESS
        self.valor = 0

    def leer(self):
        """ Función que lee los datos del sensor. """
        try:
            data = self.I2Cbus.read_i2c_block_data(self.I2C_SLAVE_ADDRESS,0x00,16)
            print("Recibido desde Arduino:")
            print(data)
            # convierte los datos y los procesa
            data = procesarDatoSensor(str(data))
            self.valor = data
            return data
        except:
            print("Error de lectura")
            # Se limita a un entero con signo, asumiendo que el rango del sensor es de 0 a 100°C. El -99 indica un error.
            self.valor = -99
            time.sleep(0.5)
            return -1
    
    def valor(self):
        """ Función que retorna el valor del sensor. """
        return self.valor

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
                sensor = Sensor(I2Cbus, I2C_SLAVE_ADDRESS)
                #se invoca el método de la clase para que obtenga el valor del sensor
                sensor.leer()
                print("Recibido desde Arduino:")
                print(sensor.valor)
            except:
                print("Error de lectura")
                time.sleep(0.5)
   
if __name__ == '__main__':
    while True:
        # ejecuta la función principal cada 1 segundo
        main()
        time.sleep(1)
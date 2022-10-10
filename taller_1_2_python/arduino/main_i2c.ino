/* Programa principal para el Arduino UNO
Genera una conexión a través del bus I2C, y envía números aleatorios a través de este, considerando una resolución de 10 bits.

Autores: Juan Carlos Muñoz
         José Henríquez
*/

#include <Arduino.h>
#include <Wire.h>

void enviarDato();

void setup() {
    //Configurar i2c como esclavo
    Wire.begin(8); // dirección 8
    Wire.onRequest(enviarDato); // función que se ejecuta cuando el maestro solicita datos
}

void loop() {
    // Esperando callback onRequest
}

void enviarDatos(){
    int dato = random(0, 1023); // genera un número aleatorio entre 0 y 1023
    //Concatenar 'val:' con el dato
    String datoString = "val:" + String(dato);
    //Enviar el dato en 6 bytes
    Wire.write(datoString.c_str(), 6);
}
/* Programa principal para el Arduino UNO
Genera una conexión a través del UART, y envía números aleatorios a través de este, considerando una resolución de 10 bits.
Además de esto, se encarga de recibir los datos que se envían desde el computador mediante la interfaz USB-TTL,
y los envía mediante el puerto serial.

Autores: Juan Carlos Muñoz
         José Henríquez
*/

#include <Arduino.h>

// la función millis() retorna unsigned long
unsigned long tiempoInicio; 
unsigned long tiempoDelay;
unsigned long tiempoActual;

void setup() {
    Serial.begin(9600);
    Serial.println("Iniciando conexión serial...");
    Serial.println("Terminal: Arduino UNO - 9600 baudios");
    Serial.println("Escuchando instrucciones...");
    Serial.println("Enviando datos...");

    tiempoDelay = 1000; // tiempo de delay en milisegundos
	tiempoActual = millis();
	tiempoInicio = tiempoActual; 
}

void enviarDatos(){
    int dato = random(0, 1023); // genera un número aleatorio entre 0 y 1023
    //Concatenar 'val:' con el dato
    Serial.print("val:");
    Serial.println(dato);
}

void loop() {   

    tiempoActual = millis(); // por cada ciclo se actualiza la variable

	if (tiempoActual - tiempoInicio >= tiempoDelay) { // si el tiempo actual es mayor al tiempo de inicio más el tiempo de delay
		enviarDatos(); //Lee el sensor y envía los datos
		tiempoInicio = tiempoActual;  // el contador se vuelve a cero
	}

    if (Serial.available() > 0) { // si hay datos en el buffer de entrada
        String entrada = Serial.readString(); // lee los datos
        Serial.println(entrada); // imprime los datos por serial
    }
}
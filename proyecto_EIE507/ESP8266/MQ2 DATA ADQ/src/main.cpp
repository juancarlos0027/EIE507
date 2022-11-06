#include <Arduino.h>
#include <time.h>

const int RL = 956; // Resistencia de carga de 956 ohms, medidos con multímetro.
float promediarADC();
double leerNivelCO(float Vout);

void setup() {
  // Configuración del puerto A0 como entrada para el sensor MQ2
  pinMode(A0, INPUT);
  // Inicializa el puerto serial en 9600 baudios
  Serial.begin(9600);
}

void loop() {

  // Lee el valor promedio de 5 ciclos, del sensor MQ2
  int sensorValue = 0;
  sensorValue = promediarADC();

  float sensorVoltage = sensorValue * (3.3 / 1023.0);
  double valorPPM = leerNivelCO(sensorVoltage);

  // Imprime el valor del sensor en el puerto serial
  /* Serial.print("Valor leido: ");
  Serial.println(sensorValue);
  Serial.print("Voltaje: ");
  Serial.println(sensorVoltage);
  Serial.print("Nivel de CO : ");
  Serial.print(valorPPM);
  Serial.println(" PPM"); */

  // Se envía el valor del sensor por el puerto serial con el formato de
  // MQ2:valorPPM 

  // Concatenar el valor del sensor con el prefijo "MQ2:" y acondicionar la cadena para que sea recibida por la raspberry pi
  String valorSensor = "MQ2:" + String(valorPPM);
  valorSensor.replace(".", ",");
  valorSensor.replace(" ", "");

  // Imprime el valor del sensor en el puerto serial
  Serial.println(valorSensor);
  
  // Espera 5 segundo
  delay(5000);
  
}

float promediarADC(){
  float promedio = 0;
  for (int i = 0; i < 10; i++)
  {
    promedio += analogRead(A0);
  }
  return promedio/10.0;
}

double leerNivelCO(float Vout){

  // Ecuacion de la curva de calibracion, mediante series de potencias, y tomando los puntos desde el datasheet
  // 38760x^-3,13 = Y (Obtenido mediante regresión por series de potencias usando Google Sheets)
  // x=(Rs/Ro)

  // RL: Resistencia de carga de 956 ohms, medidos con multímetro entre el pin A0 y GND

  // Rs = RL * ((Vref - Vout)/Vout))) => Vout es el voltaje de salida del sensor
  // Rs = RL * ((3.3 - Vout)/Vout)))
  // Rs = 956*((3.3 - 0.36)/0.36)))) Cuando el aire esta limpio
  // A aproximadamente 1000PPM de CO, el sensor tiene una resistencia Rs de 7807 ohms => Ro = 2439 ohms

  float Rs = RL*((3.3-Vout)/Vout);
  double nivelDeCO = 38760*pow((Rs/(float)2439), -3.13);

  return nivelDeCO;
}
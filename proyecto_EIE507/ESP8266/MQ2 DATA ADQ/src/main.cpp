#include <Arduino.h>
#include <time.h>
#include <ESP8266WiFi.h> // WiFi driver
#include <ESP8266HTTPClient.h> // HTTP client

const int RL = 956; // Resistencia de carga de 956 ohms, medidos con multímetro.
float promediarADC();
double leerNivelCO(float Vout);

const char* ssid = "";
const char* password = "";

void setup() {
  HTTPClient http;

  // Configura la conexión WiFi a la red
  WiFi.begin(ssid, password);
  Serial.println("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Dirección IP: ");
  Serial.println(WiFi.localIP());

  // Configuración del puerto A0 como entrada para el sensor MQ2 con SoftwareSerial
  pinMode(A0, INPUT);

}

void loop() {

  // Lee el valor promedio de 5 ciclos, del sensor MQ2
  int sensorValue = 0;
  sensorValue = promediarADC();

  float sensorVoltage = sensorValue * (3.3 / 1023.0);
  double valorPPM = leerNivelCO(sensorVoltage);

  // Publicar a través de POST
  HTTPClient http;
  http.begin("http://192.168.1.3:3000/api/CO"); // HTTP
  http.addHeader("Content-Type", "application/json");
  String payload = "{\"valor\":" + String(valorPPM) + "}";
  

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
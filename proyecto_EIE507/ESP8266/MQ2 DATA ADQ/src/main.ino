#include <Arduino.h>
#include <time.h>
#include <ESP8266WiFi.h> // WiFi driver
#include <ESP8266HTTPClient.h> // HTTP client

const int RL = 956; // Resistencia de carga de 956 ohms, medidos con multímetro.
float promediarADC();
double leerNivelCO(float Vout);

// Configuración de parámetros del dispositivo
const String device_id = "1";


// Configuración de red
const char* ssid = "";
const char* password = "";
const String api_server = "http://192.168.1.3:8000";

void setup() {
    Serial.begin(115200);
    Serial.println("Iniciando dispositivo");
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

    // cast double a String
    String valorPPMString = String(valorPPM, 2);

    if(WiFi.status()== WL_CONNECTED){
        WiFiClient client;
        HTTPClient http;

        // Primero obtener la cookie de sesión
        http.begin(client, api_server + "/sanctum/csrf-cookie");

        // Buscar el valor de la cookie de sesión
        int httpCode = http.GET();

        if (httpCode > 0) {
            // Obtener la cookie de sesión
            String cookie = http.header("Set-Cookie");
            
            // Extraer el valor de XSRF-TOKEN dentro de la cookie, desde después del signo = hasta justo antes del signo %
            // CSRF
            int pos = cookie.indexOf("XSRF-TOKEN");

            // Desde la posición pos + 11, hasta justo antes del signo %
            String csrf_token = cookie.substring(pos + 11, cookie.indexOf("%", pos + 11));


 
            // Cerrar la conexión
            http.end();

            // Enviar los datos al servidor
            http.begin(client, api_server + "/api/mediciones");
            http.addHeader("Content-Type", "application/json");
            http.addHeader("Accept", "application/json");
            http.addHeader("X-XSRF-TOKEN", xsrf_token);

            // Crear el JSON con los datos
            String payload = "{\"sensor_id\":" + device_id + ", \"measure_unit_id\": 1, \"amount\":" + valorPPMString + "}";
            //Serial.println("JSON: " + payload);

            // Enviar el JSON
            httpCode = http.POST(payload);

            if (httpCode > 0) {
                String payload = http.getString();
                Serial.println("Respuesta del servidor: " + payload);
            } else {
                Serial.println("Error al enviar los datos al servidor");
            }
        } else {
            Serial.println("Error al obtener la cookie de sesión");
        }

        http.end();
    }
    else {
        Serial.println("WiFi Desconectado");
    }

  // Publicar a través de POST

    

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
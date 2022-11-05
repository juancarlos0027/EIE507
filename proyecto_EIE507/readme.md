**Proyecto final del curso EIE507 - Sistemas embebidos**
*Estudiantes: 
-José Henríquez 
-Juan Carlos Muñoz

*Descripción*
El siguiente proyecto para el curso de sistemas embebidos, consiste en un sistema adquisidor de datos para medir la calidad del aire ambiental. Para ello se sirve de un módulo MQ-2, configurando su sensibilidad para que los datos leídos correspondan a los del nivel de CO en el aire. Esta información se transmite de manera analógica hacia el microcontrolador de un ESP8266. Este microprocesador cuenta en un reducido espacio, periféricos como 1 UART físico, 1 ADC, y en caso de escalar la aplicación, podría considerarse la utilización del módulo WiFi que integra.

La información que recibe el microprocesador, es acondicionada para enviarla hacia un microservidor mediante comunicación serial. Para este desarrollo, se utiliza una tarjeta Raspberry Pi 4 model B como microservidor, y en primera instancia, para la primera entrega del proyecto, considera únicamente la recepción de la información, para luego en una segunda entraga, almacenarla en una base de datos, con la posibilidad de acceder a la información en el navegador web.

*Aspectos técnicos*
-Para la programación del ESP8266, se utiliza VScode en conjunto con PlatformIO, utilizando el framework de Arduino.
-La programación desde el lado de la Raspberry Pi, se realiza en Python, principalmente a la escucha del puerto serial.
Welcome to the MISW4201-202311-Backend-Grupo14 wiki!


## Miembros del Grupo 12:
| # | Nombres | Correo |
|---|---------------|---------------|
| 1 | Andres Ulloa | a.ulloar  |
| 2 | Jorge Pardo | ja.pardor1  |
| 3 | Roberto Amin | r.amin  |


## Descripcion y Diseño

### Tacticas para favorecer la Disponibilidad

Creamos una arquitectura de microservicios con tacticas de:
API Gateway que permite separar los microservicios entre si, creando un desacoplamiento
Introduccion de CQRS para separar los commandos de las consultas, para esto creamos 2 segmentos de microservicios separados con objetivos distintos
Introduccion de redundancia activa impar (3) en los microservicios de consulta, de esta manera, tenemos un principal 
y si este falla los otros 2 actuan de respaldo Introduccion de una tactica de monitor ping-echo, 
en donde un componente monitor envia un señal alive a cada microservicio y estos contestan con un codigo 200 si estan disponibles.

De esta forma, por un lado identificabamos las fallas de disponibilidad (falla = microservicio fuera de servicio), 
una vez identificada, el API Gateway permitia el re-enrutamiento de consultas a otro microservicio disponible en una 
tactica de redundancia activa impar, y cuando el microservicio afectado se recuperaba, el mismo API gateway que enmascaraba 
las fallas al usuario, redireccionaba las peticiones al microservicio de consulta principal en nuestra arquitectura… 
Esto permitio tanto detectar como enmascarar y ofrecer asi una disponibilidad superior al 90% que esperabamos en el experimento. 
Sin embargo, se nota cierta latencia que podria afectar la disponibilidad en un momento dado.


![diagrama_experimento](https://user-images.githubusercontent.com/111446386/226238489-98f571ea-d8c1-4989-883c-451f0c17a738.jpg)


Los resultados del experimento se encuentran el archivo Log, ubicado en este repositorio: 
https://github.com/AndresFUlloa/jupiter-ccp-microservices/blob/develop/Microservicios/ApiGateway/Monitor/flaskr/20230227012641log.txt: ![image](https://user-images.githubusercontent.com/111446386/221460123-dd7432ab-c8c5-4c48-b20f-3086486918f4.png)

Video Demo del experimento:
https://uniandes-my.sharepoint.com/:v:/g/personal/r_amin_uniandes_edu_co/EaQ17BfvsiVAni-grrS18kgBKTZvI8eHJf__Ys2-k4Ek8w?e=S144Jm

Ambiente:
1. El codigo esta desarrollado en Python 3.11 y se corrio en Windows 11
2. Se anexa el requirements.txt con las librerias requeridas
3. Se utilizo una unica base de datos para todos los microservicios
4. Cada microservicio se corre en una terminal separada en puertos diferentes, se debe ubicar en cada directorio del microservicio y ejecutar de la siguiente forma:
  Microservicio ventasCommand: flask run -p 5004
  Microservicio microservicio_consul_1: flask run -p 5001
  Microservicio microservicio_consul_2: flask run -p 5002
  Microservicio microservicio_consul_3: flask run -p 5003
  API Gateway apigate: flask run -p 5006
  Monitor flaskr:      flask run -p 5000
  
### Tacticas de seguridad
Creamos una arquitectura de microservicios con tácticas de:
API Gateway que permite separar los microservicios entre si, creando un desacoplamiento, Introducción de una cola de mensajes que incorpora comunicación asincrónica entre el microservicio de ventas y el de Bodega, encolando así los mensajes de pedidos enviados, de esta manera evitamos saturar el canal hacia la bodega
Introducción de un elemento Certificador a través de JWT desde el login en un componente autenticador, usando un JWT_SECRET_KEY que permite únicamente a los componentes que la obtengan certificarse para interactuar en la solución.
Introducción de tokens de autorización (utilizando JWT) en los métodos de generación de pedidos y consultas entre el API Gateway, el micro de Ventas y el micro de Bodega usando la cola de mensajes como intermediario, cada uno debía tener su token de acceso y este era validado a su vez por el servicio que recibía el mensaje.

De esta forma, logramos una seguridad integral en nuestra aplicación, al No solo certificar a los usuarios (saber quienes son), sino además, establecer canales de comunicación seguros a través de tokens que permiten accesos únicamente a los usuarios habilitados con dichos permisos en nuestra arquitectura (Ej, Vendedor en modulo de ventas, y Bodeguero en modulo de Inventarios).  Esto permitio tanto detectar como habilitar permisos y ofrecer asi un control de acceso superior al 90% que esperabamos en el experimento. 

[![Diagrama experimento seguridad](https://user-images.githubusercontent.com/111446386/226237078-44563246-db37-49e9-8fa0-61309828484a.jpg)](https://uniandes-my.sharepoint.com/personal/r_amin_uniandes_edu_co/_layouts/15/stream.aspx?id=%2Fpersonal%2Fr%5Famin%5Funiandes%5Fedu%5Fco%2FDocuments%2FDemo%20experimento%20seguridad%2Emp4&wdLOR=c33D8B7B0%2DAE14%2D4E8D%2D9950%2D30354D6F3030&ga=1)

Video Demo del experimento:
https://uniandes-my.sharepoint.com/:v:/g/personal/r_amin_uniandes_edu_co/EfiAWXmZgt9DhbyilgCECEoB4YtIpPODRXMlrI4DVR8CAQ?e=f5As18

Ambiente:
1. El codigo esta desarrollado en Python 3.11 y se corrio en Windows 11
2. Se utilizo una unica base de datos para todos los microservicios, y otra base de datos para el autenticador de usuarios
3. Cada microservicio se corre en una terminal separada en puertos diferentes, se debe ubicar en cada directorio del microservicio y ejecutar de la siguiente forma:
  Microservicio ventasCommand: flask run -p 5000
  Microservicio Bodegar: flask run -p 5006
  Microservicio Autenticador: flask run -p 5008
  API Gateway apigate: flask run -p 5001
  cola de mensajes:      flask run -p 5007
  Archivo Task (tareas en directorio cola de mensajes):  python task.py
4. La tabulacion de las pruebas y resultados se anexa en: https://uniandes-my.sharepoint.com/:x:/g/personal/r_amin_uniandes_edu_co/EZlYLVVI9mBOgRUx1Sp6GzcBy6qvoXCvTJSbPYNIPpQG_g?e=ZEjTEd&wdLOR=c212DE98C-A81F-48A5-BC90-30BD9BD92BF8


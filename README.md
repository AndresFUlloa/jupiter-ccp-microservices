Welcome to the MISW4201-202311-Backend-Grupo14 wiki!


### Miembros del Grupo 12:
| # | Nombres | Correo |
|---|---------------|---------------|
| 1 | Andres Ulloa | a.ulloar  |
| 2 | Jorge Pardo | ja.pardor1  |
| 3 | Roberto Amin | r.amin  |


### Descripcion y Diseño

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
![diagrama_experimento](https://user-images.githubusercontent.com/111446386/221460027-0b737a8d-2090-4350-bb6b-ebf4d9e34946.jpg)


Los resultados del experimento se encuentran el archivo Log, ubicado en este repositorio: 
https://github.com/AndresFUlloa/jupiter-ccp-microservices/blob/develop/Microservicios/ApiGateway/Monitor/flaskr/20230227012641log.txt: ![image](https://user-images.githubusercontent.com/111446386/221460123-dd7432ab-c8c5-4c48-b20f-3086486918f4.png)

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
  

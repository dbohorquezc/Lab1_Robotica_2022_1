<h1 align="center"; style="text-align:center;">Laboratorio 1: Introducción ROS</h1>
<p align="center";style="font-size:50px; background-color:pink; color:red; text-align:center;line-height : 60px; margin : 0; padding : 0;">
Robótica</p1>
<p align="center";style="font-size:50px; text-align:center; line-height : 40px;  margin-top : 0; margin-bottom : 0; "> <br> Giovanni Andrés Páez Ujueta</p>
<p align="center";style="font-size:50px; text-align:center; line-height : 20px; margin-top : 0; "> email: gpaezu@unal.edu.co</p>
<p align="center"; style="font-size:50px; text-align:center; line-height : 40px;  margin-top : 0; margin-bottom : 0; "> <br> Daniel Esteban Bohorquez Cifuentes</p>
<p align="center"; style="font-size:50px; text-align:center; line-height : 20px; margin-top : 0; "> email: dbohorquezc@unal.edu.co</p>
<p align="center"; style="font-size:50px; text-align:center; line-height : 30px;  margin-top : 0; margin-bottom : 0; "> <br><br>INGENIERÍA MECATRÓNICA</p>
<p align="center"; style="font-size:50px; text-align:center; line-height : 30px; margin-top : 0; "> Facultad de Ingeniería</p>
<p align="center"; style="font-size:50px; text-align:center; line-height : 30px; margin-top : 0; "> Universidad Nacional de Colombia Sede Bogotá</p>
<br>
<p align="center">
  <img align="center"; width="100" height="100" src="Fig/Escudo_UN.png">
</p>

<p align="center"; style="font-size:50px; text-align:center; line-height : 30px; margin-top : 0; "> <br>7 de abril de 2022</p>



## Ejercicio en Matlab
En el primer ejercicio se hace uso de la herramienta Matlab la cual permite por medio de una de sus librerías tener una conxecion con ROS, para realizar eesto se inicia con el siguiente comando:
```console
rosinit; Conexión con el nodo maestro
```
Para comprobar esta configuracion se utiliza la interfaz visual de ROS para obtener los nodos en funcionamiento y de esta manera evideciar un componente de Matlab conectado al nodo maestro. La siguiente parte permite ingresar al tópico de velocidad y publicar un mensaje que cambia la velocidad inicial linear en X.
```console
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); %Creación publicador
velMsg = rosmessage(velPub); %Creación de mensaje
velMsg.Linear.X = 1; %Valor del mensaje
send(velPub,velMsg); %Envio
pause(1)
```
Es necesario tener en cuenta que en algunos casos no se necesita modificar los valores de velocidad o posición y en cambio solo se necesita una lectura que se puede realizar por medio de una subscripción al tópico, para esto se agregaron las siguientes lineas:
```console
a=rossubscriber("/turtle1/pose","turtlesim/Pose");
PosX=a.LatestMessage.X
```
Se evidencia la subscripción mencionada y una variable PosX que para Matlab es una variable que muestra en pantalla.

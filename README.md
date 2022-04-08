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

## Metodología

### Primer punto (MATLAB)

* En ubuntu, se lazó una terminal para ingresar el comando *roscore*, y así inicializar el nodo maestro.
* En una segunda terminal se escribe el comando *rosrun turtlesim turtlesim node* para ejecutar turtlesim.
* En MATLAB se creo un  script con el codigo dado en la guía.

```
%%
rosinit; %Conexi ́on con nodo maestro
%%
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); %Creaci ́on publicador
velMsg = rosmessage(velPub); %Creaci ́on de mensaje
%%
velMsg.Linear.X = 1; %Valor del mensaje
send(velPub,velMsg); %Envio
pause(1)
``` 
Para comprobar esta configuracion se utiliza la interfaz visual de ROS, en la que s epuede obtener informacion de los nodos en funcionamiento, y así evideciar que esté el componente de Matlab conectado al nodo maestro. Al ejecutar  se observó como la tortuga avanzaba en su eje x relativo, es decir, hacia el frente una unidad.

* Se creo las siguientes lineas de código para suscribirse al tópico de pose
 
 ```
a=rossubscriber("/turtle1/pose","turtlesim/Pose");
PosX=a.LatestMessage.X
 ``` 
Cabe resaltar que solo se debe suscribir una vez al nodo, por lo que si queremos saber repetidas veces la ubicacion de la tortuga debemos ejecutar la ultima linea de codigo.
*  se realizaron  las siguientes lineas de código para  permitir enviar datos a los valores de la pose de turtle1, por medio del servicio de Teleport Absolut, para esto es necesario crear un cliente que acceda al servicio, y al igual que en el topico, crear un mensaje de envio en el que se le indica los argumentos X, Y y Theta.

Se evidencia la subscripción mencionada y una variable PosX que para Matlab es una variable que muestra en pantalla. Ahora se realiza un codigo que permita hacer uso del servicio de Teleport Absolute, para lo cual es necesario  crear un cliente al cual se acceda a dicho servicio y al igual que en el topico crear un mensaje de envio con el cual se le indica los argumentos, que para este caso es X, Y y Theta. 
  ```
Client = rossvcclient('/turtle1/teleport_absolute');
msg=rosmessage(Client);
msg.X=3;
msg.Y=3;
msg.Theta=2;
response=call(Client,msg);
pause(1
 
 ``` 
 Finalmente se usa el siguiente comando para finalizar la conexion del nodo maestro con MATLAB, en este caso esta comentado para relizar más modificaciones de posición si asi se desea.
```console
%%
%rosshutdown
```
 
 ### Segundo punto (Python)

 ```
 #!/usr/bin/env python3
from pynput.keyboard import Key, Listener
import rospy
import numpy as np
from geometry_msgs.msg import Twist 
import termios, sys, os
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import TeleportRelative
TERMIOS = termios
 ``` 
 ```
 def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c
 ```  
 ``` 
 def teleport(x, y, ang):
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleportA = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        resp1 = teleportA(x, y, ang)
        print('Teleported to x: {}, y: {}, ang: {}'.format(str(x),str(y),str(ang)))
    except rospy.ServiceException as e:
        print(str(e))
 ```
 ```
 def teleportRel(x,ang):
    rospy.wait_for_service('/turtle1/teleport_relative')
    try:
        teleportR = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        resp1 = teleportR(x, ang)
        
    except rospy.ServiceException:
        pass
 ``` 
 ```
 def pubVel(vel_x, ang_z, t):
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('velPub', anonymous=False)
    vel = Twist()
    vel.linear.x = vel_x
    vel.angular.z = ang_z
    #rospy.loginfo(vel)
    endTime = rospy.Time.now() + rospy.Duration(t)
    while rospy.Time.now() < endTime:
        pub.publish(vel)
 ``` 

 ``` 
 if __name__ == '__main__':
    pubVel(0,0,0.1)
    try:
        while(1):
            Tec=getkey()
            if Tec==b'w':
                pubVel(0.5,0,0.01)
            if Tec==b'a':
                pubVel(0,0.5,0.01)
            if Tec==b's':
                pubVel(-0.5,0,0.01)
            if Tec==b'd':
                pubVel(0,-0.5,0.01)
            if Tec==b' ':
                teleportRel(0,np.pi)
            if Tec==b'r':
                teleport(5.544445,5.544445,0)
            if Tec==b'\x1b':
                break                    
            

    except rospy.ROSInterruptException:
        pass 
 ```
 ## Análisis y Resultados
 
 ## conclusiones

* Se comprobó como MATLAB es una herramienta util para tener interacciones con los nodos de Ros, de tal forma que se pudo conectar, deconectar el nodo de MATLAB y realizar publicaciones y subscripciones.
* Se experimentó en general una facilidad de conexion en MATALB, aun que no había mucha literatura para realizar investigaciones. Comporado con python tine tiempos de ejecucion más lentos, python se siente más escalable por la cantidad de librerías que tiene para aportar, pero es necesario conocer adecuadamente cada funcion para realizar conexion y posteriormente publicaciones subscripciones.
* Se culmino satisfactoriamente el reto propuesto tanto en MAtlab como en Python, teniendo unn buena introduccion a la implmentacion de ROS en estos lenguajes.

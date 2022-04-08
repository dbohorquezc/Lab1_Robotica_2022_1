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

**1.**  En el SO Ubuntu, se lazó una terminal para ingresar el comando *roscore*, y así inicializar el nodo maestro.

**2.** En una segunda terminal se escribe el comando *rosrun turtlesim turtlesim node* para ejecutar turtlesim.

**3.** En MATLAB se creo un  script con el siguiente codigo (dado en la guía), con el objetivo de empezar conexion con el nodo de ROS y mover la tortuga.

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
Para comprobar la configuracion se utiliza la interfaz visual de ROS, ya que  se puede obtener informacion de los nodos en funcionamiento; y así evideciar que esté el componente de Matlab conectado al nodo de turtlesim. Al ejecutar  se observó como la tortuga avanzaba en su eje x relativo, es decir, hacia el frente una unidad.

**4.** Se agregó las siguientes lineas de código para suscribirse al tópico de pose.
 
 ```
a=rossubscriber("/turtle1/pose","turtlesim/Pose");
PosX=a.LatestMessage.X
 ```
Se evidencia la subscripción mencionada y una variable PosX para mostrar el útimo mensaje en pantalla.

**5.**  se realizaron  las siguientes lineas de código para  permitir enviar datos a los valores de la pose de turtle1, por medio del servicio de Teleport Absolut. Para esto es necesario crear un cliente que acceda al servicio, y al igual que en el topico, crear un mensaje de envio en el que se le indica los argumentos X, Y y Theta.


  ```
Client = rossvcclient('/turtle1/teleport_absolute');
msg=rosmessage(Client);
msg.X=3;
msg.Y=3;
msg.Theta=2;
response=call(Client,msg);
pause(1
 
 ``` 
**6.**  Finalmente se usa el siguiente comando para finalizar la conexion del nodo de Turtlesim con MATLAB, en este caso está comentado para relizar más modificaciones de posición si asi se desea.
```console
%%
%rosshutdown
```
 
 ### Segundo punto (Python)
**1.** Se importarón las librerías necesarías para la ejecucion del programa.
 ```
 #!/usr/bin/env python3
import rospy
import numpy as np
from geometry_msgs.msg import Twist 
import termios, sys, os
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import TeleportRelative
TERMIOS = termios
 ``` 
 **2.** Se agrega la siguiente función que cumple con recibir las teclas pulsadas en la terminal de VS y así interpretarlas y posteriormente realizar una accion.
 
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
 
 **2.** Se realiza la conexion  al servicio de teleport_absolute, que va a ser usado para el caso en que se oprima la tecla R.
 
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
 
 **3.** Se añade el código que permite la conexion al servicio de teleport_relative, que va a ser usado para el caso en que se oprima la tecla SPACE.
 
 ```
 def teleportRel(x,ang):
    rospy.wait_for_service('/turtle1/teleport_relative')
    try:
        teleportR = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        resp1 = teleportR(x, ang)
        
    except rospy.ServiceException:
        pass
 ``` 
 
 **4.** A continuacion se muestra la funcion que permite publicar la velocidad la cual será necesaría para el caso en que se opriman las teclas W, A, S y D.
 
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
**5.** Finalmente  se pone cada uno de los casos con su correspondiente funcion y valores de entrada.
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
 
 **6.** Se incluye el script realizado (*myTeleopKey.py*) al artchivo CMakeLists.txt.
 
 **7.** En una terminal se ingresa el comando *catkin make* para guardar los cambios realizados
 
 **8.** Se realiza las pruebas del codigo ejecutando Turtlesim, suceando y corriendo el archivo creado con el comando *rosrun hello turtle myTeleopKey.py*.
 
 ## Análisis y Resultados
 
 ### Primer punto (MATLAB)
 * No es posible suscribirse dos veces de seguida a un nodo, ya que si se quiere revisar ejemplo *pose* es recomendable entonces volver a ejecutar el comando para visualizar el último mensaje obtenido, ya que al estar suscrito y volver a suscribirse va a producir un error
 * Es necesario crear un cliente para realizar una publiacion, esto se ve en la línea de código mostrada en la sección anterior.
 
 ### Segundo punto (Python)

 
 ## conclusiones

* Se comprobó como MATLAB es una herramienta util para tener interacciones con los nodos de Ros, de tal forma que se pudo conectar, deconectar el nodo de MATLAB y realizar publicaciones y subscripciones.
* Se experimentó en general una facilidad de conexion en MATALB, aun que no había mucha literatura para realizar investigaciones. Comporado con python tine tiempos de ejecucion más lentos, python se siente más escalable por la cantidad de librerías que tiene para aportar, pero es necesario conocer adecuadamente cada funcion para realizar conexion y posteriormente publicaciones subscripciones.
* Se culmino satisfactoriamente el reto propuesto tanto en MAtlab como en Python, teniendo unn buena introduccion a la implmentacion de ROS en estos lenguajes.

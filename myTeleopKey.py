#!/usr/bin/env python3
from pynput.keyboard import Key, Listener
import rospy
import numpy as np
from geometry_msgs.msg import Twist 
import termios, sys, os
from turtlesim.srv import TeleportAbsolute
TERMIOS = termios

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

def teleport(x, y, ang):
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleportA = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        resp1 = teleportA(x, y, ang)
        print('Teleported to x: {}, y: {}, ang: {}'.format(str(x),str(y),str(ang)))
    except rospy.ServiceException as e:
        print(str(e))


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
                pubVel(0,np.pi,1)
            if Tec==b'r':
                teleport(5.544445,5.544445,0)
            if Tec==b'\x1b':
                break                    
            

    except rospy.ROSInterruptException:
        pass 
        
        
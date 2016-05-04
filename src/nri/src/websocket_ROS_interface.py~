#!/usr/bin/env python

import rospy
import json

from geometry_msgs.msg import Twist
from std_msgs.msg import String as ros_string


# from std_msgs.msg import Int8 as Int

class twistMessage:
    def __init__(self):
        self.linear_x = 0
        self.angular_z = 0


def get_twist_msg(data, twist_mem):
    print data
    device= data['Device']
    control= data['ControlLevel']




    twist = Twist()
    if control == 1:
        if device == "SmartPhone":
            vel = float(data['VEL'])
            theta = float(data['ANGLE'])
            twist.linear.x = vel
            twist.angular.z = theta

        else:
            vel = float(data['BETA'])*0.1
            stop_cmd = data['ControlLevel']
            bezelR = int(data['Clockwise'])
            bezelL = int(data['CounterClockwise'])
            swipeL = data['SwipeLeft']
            swipeR = data['SwipeRight']
            tap = data['Press']
            longPress = data['LongHold']
            mode = data['ControlLevel']
            #if swipeR == 1:

            #    twist_mem.linear_x += 0.1
            twist.linear.x = vel*(-1)#twist_mem.linear_x

            #elif swipeL == 1:

            #    twist_mem.linear_x -= 0.1
            #    twist.linear.x = twist_mem.linear_x
            #else:
             #   twist.linear.x = twist_mem.linear_x

    #        if stop_cmd == 0:
     #           twist.angular.z = 0
      #          twist_mem.angular_z = 0

            if bezelL == 1:
                #if mode == 1:
                twist_mem.angular_z += 0.2
                #else:
                #twist_mem.angular_z = 0.7
                twist.angular.z = twist_mem.angular_z

            elif bezelR == 1:
                #if mode == 1:
                twist_mem.angular_z -= 0.2
                #else:
                #twist_mem.angular_z = -0.7
                twist.angular.z = twist_mem.angular_z

    #        elif tap == 1:
    #            twist_mem.angular_z = 0
    #            twist.angular.z = twist_mem.angular_z

            else:
                #if mode == 1:
                twist.angular.z = twist_mem.angular_z
                #elif mode == 2:
                #    twist.angular.z = 0
                #else:
                #twist.angular.z = 0

            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x = 0
            twist.angular.y = 0

    else:
        twist.linear.x = 0
        twist_mem.linear_x = 0
        twist.angular.z = 0
        twist_mem.angular_z = 0

    #print twist
    return twist


def watch_interface(json_str, twist_mem):
    data = json.loads(json_str.data)
    #print "here"
    # pub = rospy.Publisher('cmd_vel', Twist)
    # pub = rospy.Publisher('robbie/cmd_vel', Twist)
    #pub = rospy.Publisher('/turtle1/cmd_vel', Twist)
    pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist)

    twist = Twist()

    twist = get_twist_msg(data, twist_mem)
    if not rospy.is_shutdown():
        #print "sending ", twist
        pub.publish(twist)


def listener():
    rospy.init_node('watch_interface', anonymous=True)
    tm = twistMessage()
    rospy.Subscriber("websocket_server_msgs", ros_string, watch_interface, tm)

    rospy.spin()


if __name__ == "__main__":

    try:
        listener()

    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python

import rospy
import json

from geometry_msgs.msg import Twist
from std_msgs.msg import String as ros_string

heading = 0
angle = 0
# from std_msgs.msg import Int8 as Int

class twistMessage:
    def __init__(self):
        self.linear_x = 0
        self.angular_z = 0


def get_twist_msg(data, twist_mem):
    print data
    try:
        device= data['Device']
        controlLevel= data['ControlLevel']
    except:
        device = ""
        controlLevel = 0
        vel = 0
        heading = 0
        pass

    global heading
    global angle



    twist = Twist()
    if controlLevel == 1 or device == "SmartWatch":
        if device == "SmartPhone":
            vel = float(data['VEL'])
            theta = float(data['ANGLE'])
            twist.linear.x = vel
            twist.angular.z = theta

        elif device == "SmartWatch":
            alpha = float(data['ALPHA'])
            beta = float(data['BETA'])
            bezelR = int(data['Clockwise'])
            bezelL = int(data['CounterClockwise'])


            if alpha < 5 and alpha > -5:
                vel = float(beta)*-1
                vel /= 10
                if vel < 2 and vel > -2:
                    vel = 0


                if bezelL == 1:
                    if vel != 0:
                        if heading > 0:
                            heading = 0
                        else:
                            if heading != -1:
                                heading -= 0.1
                            else:
                                heading == -1

                    #twist_mem.angular_z += 0.2
                    #else:
                    #twist_mem.angular_z = 0.7
                    #twist.angular.z = twist_mem.angular_z

                elif bezelR == 1:
                    if vel != 0:
                        if heading < 0:
                            heading = 0
                        else:
                            if heading != 1:
                                heading += 0.1
                            else:
                                heading == 1
            else:
                vel = 0
                heading = 0


            twist.linear.x = vel#twist_mem.linear_x
            twist.angular.z = heading

#            if bezelL == 1:
                #if mode == 1:
#                twist_mem.angular_z += 0.2
                #else:
                #twist_mem.angular_z = 0.7
#                twist.angular.z = twist_mem.angular_z

#            elif bezelR == 1:
                #if mode == 1:
#                twist_mem.angular_z -= 0.2
                #else:
                #twist_mem.angular_z = -0.7
#                twist.angular.z = twist_mem.angular_z

    #        elif tap == 1:
    #            twist_mem.angular_z = 0
    #            twist.angular.z = twist_mem.angular_z

 #           else:
                #if mode == 1:
 #               twist.angular.z = twist_mem.angular_z
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
    try:
        data = json.loads(json_str.data)
    except:
        data = ""
        pass
    #print "here"
    pub = rospy.Publisher('cmd_vel', Twist)

    # pub = rospy.Publisher('robbie/cmd_vel', Twist)
    #pub = rospy.Publisher('/turtle1/cmd_vel', Twist)
    #pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist)

    twist = Twist()
    if data == "":
        twist = Twist()
    else:
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

#!/usr/bin/env python

import rospy
import json

from geometry_msgs.msg import Twist
from std_msgs.msg import String as ros_string
from std_msgs.msg import Int8

heading = 0
angle = 0
controlLevel = 0

# from std_msgs.msg import Int8 as Int

class twistMessage:
    def __init__(self):
        self.linear_x = 0
        self.angular_z = 0


def get_twist_msg(data):
    global controlLevel
    #rospy.loginfo(str(data))
    try:
        device = data['Device']
        controlLevel = data['ControlLevel']
    except:
        device = ""
        controlLevel = 0
        vel = 0
        heading = 0
        pass

    global heading
    global angle



    twist = Twist()

    if controlLevel == 1:
        if device == "SmartPhone":
            vel = float(data['VEL'])
            heading = float(data['ANGLE'])
            #theta = float(data['ANGLE'])
            #twist.linear.x = vel
            #twist.angular.z = theta
            #controlLevel = controlLevel-1

        else:
            alpha = float(data['ALPHA'])
            beta = float(data['BETA'])
            bezelR = int(data['Clockwise'])
            bezelL = int(data['CounterClockwise'])

            if alpha < 5 and alpha > -5:
                vel = float(beta) * -1
                if vel < 3 and vel > -4:
                    vel = 0

                max_speed = 0.8
                vel = (vel / 10) * max_speed

                if bezelR == 1:
                    if heading > 0:
                        heading = 0
                    else:
                        if heading != -1:
                            heading -= 0.1
                        else:
                            heading = -1


                elif bezelL == 1:
                    if heading < 0:
                        heading = 0
                    else:
                        if heading != 1:
                            heading += 0.1
                        else:
                            heading = 1
            else:
                vel = 0
                heading = 0
                controlLevel=0
        #print vel, heading
        twist.linear.x = vel  # twist_mem.linear_x
        twist.angular.z = heading

        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0

    else:
        twist.linear.x = 0
        twist.angular.z = 0
        #if device=="SmartPhone" and controlLevel!=0:
        #    controlLevel=controlLevel-1

    print controlLevel
    control_pub.publish(controlLevel)
    return twist


def device_interface(json_str):
    global controlLevel
    try:
        data = json.loads(json_str.data)
    except:
        data = ""
        pass

    if data == "":
        twist = Twist()

    else:
        twist = get_twist_msg(data)
    print controlLevel


    if not rospy.is_shutdown() and controlLevel==1:
        print twist

        # print "sending ", twist
        #print twist
        pub.publish(twist)






def listener():
    rospy.Subscriber("websocket_server_msgs", ros_string, device_interface)

    rospy.spin()


if __name__ == "__main__":

    try:
        rospy.init_node('websocket_ROS_interface', anonymous=True)
        #pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist)
        pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist)
        #pub = rospy.Publisher('cmd_vel', Twist)
        control_pub = rospy.Publisher('control_level', Int8,latch=True)
        # pub = rospy.Publisher('robbie/cmd_vel', Twist)
        # pub = rospy.Publisher('/turtle1/cmd_vel', Twist)


        listener()

    except rospy.ROSInterruptException:
        pass

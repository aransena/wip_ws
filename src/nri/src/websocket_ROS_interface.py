#!/usr/bin/env python

import rospy
import json

from geometry_msgs.msg import Twist
from std_msgs.msg import String as ros_string
from std_msgs.msg import Int8

heading = 0
angle = 0
controlLevel = 0
requestLevel = 0
active_device = 0

TABLET_DEVICE_LEVEL = 4
SMARTPHONE_DEVICE_LEVEL = 3
WATCH_DEVICE_LEVEL = 2

class twistMessage:
    def __init__(self):
        self.linear_x = 0
        self.angular_z = 0


def get_twist_msg(data):
    global controlLevel
    global heading
    global angle
    global requestLevel
    device = ""
    controlLevel = 0
    vel = 0
    #heading = 0
    try:
        device = data['Device']
        controlLevel = data['ControlLevel']

    except:
        pass

    twist = Twist()

    if controlLevel > 0:
        if device == "SmartPhone":
            control_request_pub.publish(SMARTPHONE_DEVICE_LEVEL)
            requestLevel = SMARTPHONE_DEVICE_LEVEL
            vel = float(data['VEL'])
            heading = float(data['ANGLE'])

        else:
            control_request_pub.publish(WATCH_DEVICE_LEVEL)
            requestLevel = WATCH_DEVICE_LEVEL
            alpha = float(data['ALPHA'])
            beta = float(data['BETA'])
            bezelR = int(data['Clockwise'])
            bezelL = int(data['CounterClockwise'])
	    turn = float(data['Turn'])
	    mode = int(data['Mode'])

            if alpha < 5 and alpha > -5:
                vel = float(beta) * -1
                if vel < 3 and vel > -4:
                    vel = 0

                max_speed = 0.8
                vel = (vel / 10) * max_speed
                print "Heading: ", heading
                if bezelR == 1 and mode == 1:
                    if heading > 0:
                        heading = 0
                    else:
                        if heading != -1:
                            heading -= 0.1
                        else:
                            heading = -1

                elif bezelL == 1 and mode == 1:
                    if heading < 0:
                        heading = 0
                    else:
                        if heading != 1:
                            heading += 0.1
                        else:
                            heading = 1
		if mode ==2:
		    heading = turn

            if controlLevel != 1:
                vel = 0
                heading = 0

    heading_cmd = heading
    if vel < 0:
        heading_cmd = heading * -1

    twist.linear.x = vel
    twist.angular.z = heading_cmd

    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0

    return twist


def device_interface(json_str):
    global controlLevel
    global requestLevel
    global active_device
    try:
        data = json.loads(json_str.data)
    except:
        data = ""
        pass

    if data == "":
        twist = Twist()

    else:
        twist = get_twist_msg(data)

    if not rospy.is_shutdown() and active_device == requestLevel:
        # print twist
        control_pub.publish(controlLevel)
        log_str = "Control level : " + str(controlLevel) + "\nTwist: " + str(twist)
        rospy.loginfo(log_str)
        if controlLevel == 1:
            pub.publish(twist)

 #       rate.sleep()


def get_active_device(data):
    global active_device
    active_device = data.data


def listener():
    rospy.Subscriber("mux/active_device", Int8, get_active_device)
    rospy.Subscriber("websocket_server_msgs", ros_string, device_interface)
    rospy.spin()


if __name__ == "__main__":

    try:
        rospy.init_node('websocket_ROS_interface', anonymous=True)
        rospy.loginfo("Websocket server ROS interface started")
        #pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)
        pub = rospy.Publisher('/cmd_vel', Twist,queue_size=1)
        control_pub = rospy.Publisher('control_level', Int8, latch=True, queue_size=1)
        control_request_pub = rospy.Publisher('mux/control_request', Int8, latch=False, queue_size=1)
        # pub = rospy.Publisher('robbie/cmd_vel', Twist)
        # pub = rospy.Publisher('/turtle1/cmd_vel', Twist)
#        rate = rospy.Rate(200)  # 10hz

        listener()

    except rospy.ROSInterruptException:
        pass

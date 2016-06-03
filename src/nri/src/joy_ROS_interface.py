#!/usr/bin/env python

import rospy
import sys
import math

from geometry_msgs.msg import Twist
from std_msgs.msg import String as ros_string
from std_msgs.msg import Int8
from sensor_msgs.msg import Joy

heading = 0
angle = 0

controlLevel = 0
active_device = 0

max_speed = 1.0
max_rot = 1.0

DEVICE_LEVEL = 1

# from std_msgs.msg import Int8 as Int

def get_twist_msg(joy_data):
    global controlLevel
    global heading
    global angle
    global max_speed
    global max_rot

    data = Joy()
    data = joy_data

    controlLevel = 1
    controlLevel = math.fabs(int(round(pow(data.axes[5]-1,2)/4))) + math.fabs(int(round(pow(data.axes[2]-1,2)/4))) + data.buttons[4]+data.buttons[5]+1


    x = data.axes[0]
    y = data.axes[1]
    vel = y * max_speed
    heading = x * max_rot

    tol = 0.35
    if math.fabs(vel)<tol:
        vel = 0
    if vel<0:
        heading = heading*-1
    if math.fabs(heading)<tol:
        heading = 0

    twist = Twist()

    if controlLevel == 1:
        twist.linear.x = vel  # twist_mem.linear_x
        twist.angular.z = heading

    else:
        twist.linear.x = 0
        twist.angular.z = 0


    return twist


def device_interface(data):
    global controlLevel

    global active_device

    control_request_pub.publish(DEVICE_LEVEL)

    if data == "":
        twist = Twist()

    else:
        twist = get_twist_msg(data)


    if not rospy.is_shutdown() and active_device==DEVICE_LEVEL:
        #print twist
        control_pub.publish(controlLevel)
        if controlLevel==1:
            pub.publish(twist)

 #       rate.sleep()



def get_active_device(data):
    global active_device
    active_device = data.data


def listener():
    global max_speed
    global max_rot
    rospy.Subscriber("/joy", Joy, device_interface)


    print rospy.myargv(argv=sys.argv)
    try:
        args = rospy.myargv(argv=sys.argv)
        max_speed = float(args[1])
    except:
        pass
    try:
        args = rospy.myargv(argv=sys.argv)
        max_rot = float(args[2])
    except Exception as e:
        print e
        pass

    print max_speed, max_rot

    rospy.spin()


if __name__ == "__main__":

    try:
        rospy.init_node('joy_ROS_interface', anonymous=True)
        rospy.Subscriber("mux/active_device", Int8, get_active_device)

        #pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist)

        pub = rospy.Publisher('/cmd_vel', Twist, latch=True, queue_size=1)
        control_request_pub = rospy.Publisher('mux/control_request', Int8, latch=True, queue_size=1)
        control_pub = rospy.Publisher('control_level', Int8,latch=False, queue_size=1)
#        rate = rospy.Rate(100) # 100hz

        # pub = rospy.Publisher('robbie/cmd_vel', Twist)
        # pub = rospy.Publisher('/turtle1/cmd_vel', Twist)


        listener()

    except rospy.ROSInterruptException:
        pass

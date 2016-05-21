#!/usr/bin/env python

import rospy
import json

from geometry_msgs.msg import Twist
from std_msgs.msg import String as ros_string
from std_msgs.msg import Int8
heading = 0
angle = 0


# from std_msgs.msg import Int8 as Int

class twistMessage:
    def __init__(self):
        self.linear_x = 0
        self.angular_z = 0


def get_twist_msg(data, twist_mem):
    rospy.loginfo(str(data))
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

    control_pub= rospy.Publisher('control_level', Int8)
    control_pub.publish(controlLevel)

    twist = Twist()

    if controlLevel == 1 or device == "SmartWatch":
	pub = rospy.Publisher('cmd_vel', Twist)

        if device == "SmartPhone":
            vel = float(data['VEL'])
            theta = float(data['ANGLE'])
            twist.linear.x = vel
            twist.angular.z = theta


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
                vel = (vel/10) * max_speed

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

            twist.linear.x = vel  # twist_mem.linear_x
            twist.angular.z = heading

            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x = 0
            twist.angular.y = 0

    else:
	try:
		pub.unregister()
	except:
		pass
        twist.linear.x = 0
        twist_mem.linear_x = 0
        twist.angular.z = 0
        twist_mem.angular_z = 0

    # print twist
    return twist


def watch_interface(json_str, twist_mem):
    try:
        data = json.loads(json_str.data)
    except:
        data = ""
        pass

    pub = rospy.Publisher('cmd_vel', Twist)

    # pub = rospy.Publisher('robbie/cmd_vel', Twist)
    # pub = rospy.Publisher('/turtle1/cmd_vel', Twist)
    #pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist)


    if data == "":
        twist = Twist()

    else:
        twist = get_twist_msg(data, twist_mem)

    if not rospy.is_shutdown():
	
        # print "sending ", twist
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

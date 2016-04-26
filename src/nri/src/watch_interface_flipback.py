#!/usr/bin/env python

import roslib
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import String as ros_string

# from std_msgs.msg import Int8 as Int

class twistMessage:
	def __init__(self):
		self.linear_x = 0
		self.angular_z = 0

def get_twist_msg(inp, twist_mem):
	print inp
	human_control = inp[0]
	stop_cmd = inp[1]
	bezelL = inp[2]
	bezelR = inp[3]
	swipeL = inp[4]
	swipeR = inp[5]
	swipeU = inp[6]
	swipeD = inp[7]
	tap = inp[8]
	longPress = inp[9]

	twist = Twist()

	if human_control == 1:
		if stop_cmd == 1:
			twist.linear.x = 0
			twist_mem.linear_x = 0

		elif swipeR == 1:
			twist_mem.linear_x += 0.1
			twist.linear.x = twist_mem.linear_x
		elif swipeL == 1:
			twist_mem.linear_x -= 0.1
			twist.linear.x = twist_mem.linear_x

		else:
			twist.linear.x = twist_mem.linear_x

		if stop_cmd == 1:
			twist.angular.z = 0
			twist_mem.angular_z = 0

		elif bezelL == 1:
			#twist_mem.angular_z += 0.1
			twist.angular.z = 0.5#twist_mem.angular_z

		elif bezelR == 1:
			#twist_mem.angular_z -= 0.1
			twist.angular.z = -0.5#twist_mem.angular_z

		elif tap == 1:
			twist_mem.angular_z = 0
			twist.angular.z = twist_mem.angular_z

		else:
			twist.angular.z = twist_mem.angular_z


		twist.linear.y = 0
		twist.linear.z = 0
		twist.angular.x = 0
		twist.angular.y = 0


	return twist

def watch_interface(data, twist_mem):

	inp = map(int,str(data.data)[1:-1].split(",")) # converts string to int list

	#pub = rospy.Publisher('cmd_vel', Twist)
	pub = rospy.Publisher('robbie/cmd_vel', Twist)

	twist = Twist()

	twist = get_twist_msg(inp, twist_mem)

	if not rospy.is_shutdown():
		notice_str = "watch_interface: Sending cmd_vel %s" % rospy.get_time()
		#rospy.loginfo(notice_str)
		pub.publish(twist)

		# pub2.publish(0)
		#rate.sleep()


def listener():
	rospy.init_node('watch_interface', anonymous=True)
	tm = twistMessage()
	rospy.Subscriber("udp_msgs", ros_string, watch_interface, tm)

	rospy.spin()

#	rate = rospy.Rate(10)  # 10hz
#	while not rospy.is_shutdown():
		#notice_str = "watch_interface: Sending cmd_vel %s" % rospy.get_time()
		#rospy.loginfo(notice_str)
		#pub.publish(twist)
		# pub2.publish(0)
		#rate.sleep()

	## code to stop
	# twist=Twist()
	# rospy.loginfo("watch_interface: Stopping")
	# p.publish(twist)


if __name__ == "__main__":

	try:
		listener()
	except rospy.ROSInterruptException:
		pass

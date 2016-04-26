#!/usr/bin/env python

import roslib
import rospy
import socket
import sys

from std_msgs.msg import String as ros_string
#from std_msgs.msg import Int8MultiArray as ros_intArray


def udp_Connect(udp_ip, udp_port):
	rospy.loginfo("udp_listen.py: attempting connection to IP:%s Port:%d", udp_ip, udp_port)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP
	sock.bind((udp_ip, udp_port))

	rospy.loginfo("udp_listen.py: SUCCESS connecting to IP:%s Port:%d", udp_ip, udp_port)

	return sock


def broadcast_UDP(udp_ip, udp_port):
	pub = rospy.Publisher('udp_msgs', ros_string)
	rospy.init_node('udp_comms', anonymous=True)
	rospy.loginfo("udp_listen.py: udp_comms node started")

	udp_socket = udp_Connect(UDP_IP, UDP_PORT)
	#except Exception, e:
	#	rospy.logerr("udp_listen.py: FAILED connecting to IP: %s Port: %d \t error: %s", udp_ip, udp_port, e)

	while True:
		data, addr = udp_socket.recvfrom(1024)  # buffer size is 1024 bytes
		print data, " received"
		inp = data.split(",")
		inp = map(int, inp)
		print "received message:", inp
		pub.publish(str(inp))


if __name__ == "__main__":
	#args = rospy.myargv(argv=sys.argv)
	#if 1 < len(args) < 3:
	#	print "usage: my_node.py UDP_IP UDP_PORT"
	#elif len(args) == 3:
	#	UDP_IP = str(args[1])
	#	UDP_PORT = int(args[2])
	UDP_IP = "192.168.1.102"  # "192.168.43.12" #"127.0.0.1"
	#elif len(args) == 1:
	UDP_PORT = 21234
	#else:
	#print "failed to launch node - usage: `udp_listen.py UDP_IP UDP_PORT` OR `udp_listen.py`"
	#	sys.exit()
	try:
		broadcast_UDP(UDP_IP, UDP_PORT)
	except rospy.ROSInterruptException, e:
		print "failed to launch node - error ", e
		sys.exit()

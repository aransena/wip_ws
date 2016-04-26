#!/usr/bin/env python
import time
import random 

import rospy
import smach
import smach_ros
import threading
import actionlib
import subprocess

import move_base_msgs.msg as MB

from smach_ros import SimpleActionState 
from smach_ros import ServiceState
from std_msgs.msg import String

responses = ['PENDING','ACTIVE','REJECTED','SUCCEEDED','ABORTED','PREEMPTING','PREEMPTED','RECALLING','RECALLED','LOST']

goal = MB.MoveBaseGoal()
stop = bool
benchmark_state=0

def at_waypoint():
    logcommand = "rosbag record -l 1 /chatter"
    stopcommand = "rostopic pub /cmd_vel geometry_msgs/Twist '[0.0,0.0,0.0]' '[0.0,0.0,0.0]'"
    subprocess.call([logcommand],shell=True)
    subprocess.call([stopcommand],shell=True)
    rospy.wait_for_service('roah_rsbb/end_execute')

    try:
       	send_end = rospy.ServiceProxy('roah_rsbb/end_execute', SEND_END_COMMAND)
       	send_end()
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def callback_goal(data):
	global goal
	goal = data

def callback_timeoutCheck(data):
	global timeout
	timeout = data

def callback_benchmark_state(data):
	global benchmark_state
	benchmark_state = data

class initialise(smach.State):
	def __init__(self):
		smach.State.__init__(self,outcomes=['proceed','wait', 'error'])
		rospy.Subscriber("roah_rsbb/benchmark/state")


	def execute(self, userdata):
		rospy.loginfo('Executing S0_INITIAL')
		try:
			rospy.wait_for_message("/roah_rsbb/benchmark/state", BenchmarkState, 5)
			if benchmark_state == BenchmarkState.PREPARE:
				return 'proceed'
			else:
				return 'wait'
		except:
			print "PREPARE not received"

class read_rsbb(smach.State):
	def __init__(self):
		smach.State.__init__(self,outcomes=['proceed','error', 'finished'])

	def execute(self, userdata):
		rospy.loginfo('Executing S1_READ')

		rospy.Subscriber("/roah_rsbb/goal", geometry_msgs/Pose2D, callback_rsbb)	
		try:
			if benchmark_state==BenchmarkState.STOP:
				return 'finished'
			else:
				rospy.wait_for_message("/roah_rsbb/goal", geometry_msgs/Pose2D, 20)
				return 'proceed'
		except:
			print "no goal received"
			return 'error'

class set_goal(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['new_goal','error'],
									output_keys=['send_nav_goal'])
		global goal
	def execute(self, userdata):
		try:
			rospy.loginfo('Executing state S2_SET_GOAL')
			userdata.send_nav_goal = goal
			return 'new_goal'		
		except:
			return 'error'

class navigate(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['goal_reached','error'],
									input_keys=['read_nav_goal'],
									output_keys=['send_request_goal','send_current_goal'])

		self.client = actionlib.SimpleActionClient('move_base', MB.MoveBaseAction)

	def execute(self, userdata):
		rospy.loginfo('Executing state S3_NAVIGATE')
		#time.sleep(1)

		self.client.wait_for_server()
		pub = rospy.Publisher('tcd_curr_goal', geometry_msgs/Pose2D,latch=True, queue_size=10)
		pub.publish(userdata.read_nav_goal)
		self.client.send_goal(userdata.read_nav_goal)
		
		while (self.client.wait_for_result(rospy.Duration(1.0))!=True):	
			print responses[self.client.get_state()]
			rospy.Subscriber("roah_rsbb/benchmarkstate", String, callback_timeoutCheck)
			if timeout == BenchmarkState.PREPARE:
				self.client.cancel_goal()
				return 'timeout'

		result = self.client.get_state()
		if result==3: ## success
			at_waypoint()
			return 'goal_reached'
		else:
			return 'error'

class cleanup(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success_end','fail_end','error'])

	def execute(self, userdata):
		rospy.loginfo('Executing state S5_CLEANUP')
		time.sleep(1)
		if random.random()<0.5:
			return 'success_end'
		elif random.random()<0.9:
			return 'fail_end'
		else:
			return 'error'

class error_handler(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['exit'])

	def execute(self, userdata):
		rospy.loginfo('Executing state ERR')
		time.sleep(1)
		return 'exit'



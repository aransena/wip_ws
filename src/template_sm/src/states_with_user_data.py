#!/usr/bin/env python
import time
import random 
import rospy
import smach
import smach_ros



class A(smach.State):
	def __init__(self):
		smach.State.__init__(self,outcomes=['proceed','error'], output_keys=['A_out'])

	def execute(self, userdata):
		userdata.A_out = 1;
		#print(userdata.A_out)
		rospy.loginfo('Executing A')
		time.sleep(5)

		return 'proceed'

class B(smach.State):
	def __init__(self):
		smach.State.__init__(self,outcomes=['proceed','error','wait'], input_keys=['B_in'], output_keys=['B_out'])

	def execute(self, userdata):
		rospy.loginfo('Executing B')
		print(userdata.B_in)
		if userdata.B_in < 4:
			userdata.B_out=userdata.B_in+1
			time.sleep(1)
			return 'wait'
		else:
			return 'proceed'


class C(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success', 'error'])
	def execute(self, userdata):
		rospy.loginfo('Executing C')
		time.sleep(2)
		return 'success'

class D(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success','error'])

	def execute(self, userdata):
		rospy.loginfo('Executing D')
		time.sleep(2)
		return 'success'

class E(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success','error'])

	def execute(self, userdata):
		rospy.loginfo('Executing E')
		time.sleep(4)
		return 'success'

class F(smach.State):	
	def __init__(self):
		smach.State.__init__(self, outcomes=['success','error'])

	def execute(self, userdata):
		rospy.loginfo('Executing F')
		time.sleep(3)
		return 'success'

class log(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success','error'])

	def execute(self, userdata):
		rospy.loginfo('Executing state LOG')
		time.sleep(2)
		return 'success'

class cleanup(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success_end', 'error'])#,'fail_end','error'])

	def execute(self, userdata):
		rospy.loginfo('Executing state CLEANUP')
		time.sleep(2)
		return 'success_end'

class error_handler(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['exit'])

	def execute(self, userdata):
		rospy.loginfo('Executing state ERR')
		time.sleep(1)
		return 'exit'
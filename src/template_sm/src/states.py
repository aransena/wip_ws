#!/usr/bin/env python
import time
import random 
import rospy
import smach
import smach_ros

# You can have a state file for each specific state machine which you are creating, or
# you can create a shared state file which can be called from various state machines.

# Using a shared file allows you to reuse code in various state machine architectures;
# however the more states you put in a shared file, the harder it will be to follow what
# is happening in it.

# Try and use shared files for functionality which is common to multiple state machines
# and create specific states files for specific functionality.

# We are able to share the states amongst state machines, as each state is declared as an
# object-oriented class; hence the importance of using self.* for declaring any state-specific
# variables - e.g. self.counter = 0 means each state called will have it's own counter called
# self. These are declared in the state constructor __init__()

# While __init__() and execute() are the most common defs in each class, you can declare additional
# functions as required inside of that class, e.g. a function to calculate a conversion.

class A(smach.State):
	#Constructor
	def __init__(self):
		# Outcomes declared in the state must match those described in the state machine
		# proceed and error used here, but can define any number of outcomes
		smach.State.__init__(self,outcomes=['proceed','error'])

	# State functionality
	def execute(self, userdata):
		# Try/Except Python error handling - important feature to use to produce robust code
		try:
			rospy.loginfo('Executing A')
			# delays used for simulated functionality
			time.sleep(5)
			return 'proceed'

		# if an error is detected in the try section, it jumps to the except code
		except Exception,e:
			# Print out what the error was
			print"ERROR: ",str(e)
			# Transition to the error state
			return 'error'

class B(smach.State):
	def __init__(self):
		smach.State.__init__(self,outcomes=['proceed','error','wait'])

		# This time we declare a state variable and initialize it
		self.counter = 0

	def execute(self, userdata):
		try:
			rospy.loginfo('Executing B')
			# Important to always indicate we are using the state variable by using
			# "self."
			if self.counter < 4:
				self.counter +=1
				time.sleep(1)
				return 'wait'
			else:
				return 'proceed'

		except Exception,e:
			print"ERROR: ",str(e)
			return 'error'

class C(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success', 'error'])

	def execute(self, userdata):
		try:
			rospy.loginfo('Executing C')
			time.sleep(2)
			return 'success'

		except Exception,e:
			print"ERROR: ",str(e)
			return 'error'

class D(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success','error'])

	def execute(self, userdata):
		try:
			rospy.loginfo('Executing D')
			time.sleep(2)
			return 'success'

		except Exception,e:
			print"ERROR: ",str(e)
			return 'error'

class E(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success','error'])

	def execute(self, userdata):
		try:
			rospy.loginfo('Executing E')
			time.sleep(4)
			return 'success'

		except Exception,e:
			print "ERROR: ",str(e)
			return 'error'

class F(smach.State):	
	def __init__(self):
		smach.State.__init__(self, outcomes=['success','error'])

	def execute(self, userdata):
		try:
			rospy.loginfo('Executing F')
			time.sleep(3)
			return 'success'

		except Exception,e:
			print "ERROR: ",str(e)
			return 'error'

class log(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success','error'])

	def execute(self, userdata):
		try:
			rospy.loginfo('Executing state LOG')
			time.sleep(2)
			return 'success'

		except Exception,e:
			print "ERROR: ",str(e)
			return 'error'

class cleanup(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success_end', 'error'])#,'fail_end','error'])

	def execute(self, userdata):
		try:
			rospy.loginfo('Executing state CLEANUP')
			time.sleep(2)
			return 'success_end'
			
		except Exception,e:
			print "ERROR: ",str(e)
			return 'error'

class error_handler(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['exit'])

	def execute(self, userdata):
		rospy.loginfo('Executing state ERR')
		time.sleep(1)
		return 'exit'
#!/usr/bin/env python
#import roslib; roslib.load_manifest('smach_tutorials')
import rospy
import smach
import smach_ros
import time
from smach import Concurrence

class Foo(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes = ['outcome2'])
		self.counter = 0


	def execute(self, userdata):
		rospy.loginfo('Executing state FOO')
		rospy.loginfo('Counter = %f'%self.counter) 
		if self.counter < 8:
			self.counter += 1
			time.sleep(1)
			return 'still processing'
		else:
			return 'outcome2'


class Boo(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes =['outcome3'])
		self.counter = 0
	def execute(self, userdata):
		rospy.loginfo('Executing state BOO')
		rospy.loginfo('Counter = %f'%self.counter) 
		if self.counter < 6:
			self.counter = self.counter + 1
			time.sleep(1)
			return 'still processing'
		else:
			return 'outcome3'


class Idle(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes =['outcome1'])
		#self.counter = 0
	def execute(self, userdata):
		rospy.loginfo('Executing state IDLE')
		#rospy.loginfo('Counter = %f'%self.counter)
		time.sleep(6)
		return 'outcome1'

def main():
	rospy.init_node('smach_example_state_machine')

	sm = smach.StateMachine(outcomes= ['outcome6'])

	with sm:
		smach.StateMachine.add('IDLE',Idle(), transitions = {'outcome1':'CON'})

		sm_con = smach.Concurrence(outcomes = ['outcome5','outcome4'],
								   default_outcome = 'outcome4',
								   outcome_map = {'outcome5':
								   				  {'FOO':'outcome2',
								   				   'BOO':'outcome3',
								   				   'DOO':'outcome3'}})
		with sm_con:
			smach.Concurrence.add('FOO',Foo())
			smach.Concurrence.add('BOO',Boo())
			smach.Concurrence.add('DOO',Boo())

		smach.StateMachine.add('CON', sm_con, transitions={'outcome4':'CON','outcome5':'outcome6'})
	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
	sis.start()
	outcome = sm.execute()
	rospy.spin()
	sis.stop()

if __name__ == '__main__':
	main()

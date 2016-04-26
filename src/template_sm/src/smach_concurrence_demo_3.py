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

class Goo(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes =['outcome10','still_processing'])
		self.counter = 0
	def execute(self, userdata):
		rospy.loginfo('Executing state GOO')
		rospy.loginfo('Counter = %f'%self.counter) 
		if self.counter < 6:
			self.counter = self.counter + 1
			time.sleep(1)
			return 'still_processing'
		else:
			return 'outcome10'

class Hoo(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes =['outcome9','still_processing'])
		self.counter = 0
	def execute(self, userdata):
		rospy.loginfo('Executing state HOO')
		rospy.loginfo('Counter = %f'%self.counter) 
		if self.counter < 6:
			self.counter = self.counter + 1
			time.sleep(1)
			return 'still_processing'
		else:
			print 'EXECUTED'
			return 'outcome9'

class Idle(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes =['outcome1'])
		#self.counter = 0
	def execute(self, userdata):
		rospy.loginfo('Executing state IDLE')
		#rospy.loginfo('Counter = %f'%self.counter)
		time.sleep(6)
		return 'outcome1'

class Con_Con(smach.Concurrence):
	def __init__(self):
		smach.Concurrence.__init__(self, outcomes = ['outcome8','bounce'],
										 default_outcome = 'bounce',
										 outcome_map = {'outcome8':{'HOO':'outcome9',
										 							'GOO':'outcome10'},
										 				'bounce':{'HOO':'still_processing',
										 						  'GOO':'still_processing'}})
										 			
class Con(smach.Concurrence):
	def __init__(self):
		smach.Concurrence.__init__(self,outcomes = ['outcome5','outcome4'],
								   default_outcome = 'outcome4',
								   outcome_map = {'outcome5':
								   				  {'FOO':'outcome2',
								   				   'BOO':'outcome3',
								   				   'CON2':'outcome8'},
								   				   'outcome4':{'CON2':'bounce'}})


class SM(smach.StateMachine):
	def __init__(self):
		smach.StateMachine.__init__(self, outcomes = ['outcome6'])


#class SM_2(smach.StateMachine):
#	def __init__(self):
#		smach.StateMachine.__init__(self,outcomes = ['outcome5','outcome6'])


def main():
	rospy.init_node('smach_example_state_machine')

	sm = SM()
	with sm:
		smach.StateMachine.add('IDLE',Idle(), transitions = {'outcome1':'CON'})

		sm_con = Con()
		#,
								   				   #'outcome4':{'CON2':'bounce'}})
		with sm_con:
			sm_con2 = Con_Con()
			smach.Concurrence.add('FOO',Foo())
			smach.Concurrence.add('BOO',Boo())
			smach.Concurrence.add('CON2', sm_con2)

			with sm_con2:
				smach.Concurrence.add('HOO',Hoo())
				smach.Concurrence.add('GOO',Goo())
				

		smach.StateMachine.add('CON', sm_con, transitions={'outcome4':'CON','outcome5':'outcome6'})


		#

	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
	sis.start()
	outcome = sm.execute()
	rospy.spin()
	sis.stop()

if __name__ == '__main__':
	main()

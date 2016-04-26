#!/usr/bin/env python
#import roslib; roslib.load_manifest('smach_tutorials')
import rospy
import smach
import smach_ros
import time
from smach import Concurrence

class Foo(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes = ['outcome7'])
		self.counter = 0


	def execute(self, userdata):
		rospy.loginfo('Executing state FOO')
		rospy.loginfo('Counter = %f'%self.counter) 
		if self.counter < 8:
			self.counter += 1
			time.sleep(1)
			return 'still processing'
		else:
			return 'outcome7'


class Boo(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes =['outcome2'])#,'still_processing'])
		self.counter = 0
	def execute(self, userdata):
		rospy.loginfo('Executing state BOO')
		rospy.loginfo('Counter = %f'%self.counter) 
		if self.counter < 6:
			self.counter = self.counter + 1
			time.sleep(1)
		#	return 'still_processing'
		
			#print 'EXECUTED'
		#else:
		return 'outcome2'



class Hoo(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes =['outcome3','still_processing'])
		self.counter = 0
	def execute(self, userdata):
		rospy.loginfo('Executing state HOO')
		rospy.loginfo('Counter = %f'%self.counter) 
		if self.counter < 6:
			self.counter = self.counter + 1
			time.sleep(1)
			return 'still_processing'
		
			#print 'EXECUTED'
		else:
			return 'outcome3'

class Idle(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes =['outcome1'])
		#self.counter = 0
	def execute(self, userdata):
		rospy.loginfo('Executing state IDLE')
		#rospy.loginfo('Counter = %f'%self.counter)
		time.sleep(3)
		return 'outcome1'

#class Con2(smach.Concurrence):
	#sm_con2 = smach.Concurrence(outcomes = ['outcome8','outcome7'],
										#default_outcome = 'outcome7',
										#outcome_map = {'outcome8':{'HOO':'outcome10','GOO':'outcome9'}})
#	def __init__(self):
#		smach.Concurrence.__init__(self, outcomes = ['outcome8','outcome7'],
#										 default_outcome = 'outcome7',
#										 outcome_map = {'outcome8':{'HOO':'outcome9',
#										 							'GOO':'outcome10'}})
#										 				#'outcome7':{'HOO':'still processing',
										 				#'GOO':'still processing'}})
	#d	smach.StateMachine('CON2',sm_con2,transitions = {'outcome7':'CON2','outcome8':'outcome5'})
#		self.counter = 0

	#def execute(self, parent_ud = smach.UserData()):

	

	#def execute(self,userdata):
	#	time.sleep(1)
		#get_children(self)
		
	#	if self.counter < 10:
	#		self.counter = self.counter + 1
	#		return 'still processing'
	#	else:

	#	return 'processing'

 #class SM(smach.StateMachine):
 #	def __init__(self):
 #		smach.StateMachine.__init__(self, outcomes = ['outcome6'])

# 		#smach.StateMachine.add('GOO',Goo(), transitions = {'outcome10':'outcome8'})

# class SM_2(smach.StateMachine):
# 	def __init__(self):
# 		smach.StateMachine.__init__(self,outcomes = ['outcome5','outcome6'])


def main():
	rospy.init_node('smach_example_state_machine')

	#sm = smach.StateMachine(outcomes= ['outcome6'])
	sm = smach.StateMachine(outcomes = ['outcome6'])
	with sm:
		smach.StateMachine.add('IDLE',Idle(), transitions = {'outcome1':'CON'})

		sm_con = smach.Concurrence(outcomes = ['outcome5','outcome4'],
								   default_outcome = 'outcome5',
								   outcome_map = {'outcome4':{'FOO':'outcome7',
								   				  			  'SM_SUB':'outcome10'},
								   				   'outcome5':{'SM_SUB':'bounce'}})

		sm_sub = smach.StateMachine(outcomes = ['outcome10','bounce'])

		with sm_con:
			

			smach.Concurrence.add('FOO',Foo())
			smach.Concurrence.add('SM_SUB',sm_sub)
			
			with sm_sub:

				smach.StateMachine.add('BOO',Boo(), transitions = {'outcome2':'HOO'})#,'still_processing':'bounce'})
				smach.StateMachine.add('HOO',Hoo(), transitions = {'outcome3':'outcome10','still_processing':'bounce'})

			
		smach.StateMachine.add('CON', sm_con, transitions={'outcome5':'CON','outcome4':'outcome6'})


		#

	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
	sis.start()
	#sm.execute()
	#sm_con.execute()
	outcome = sm.execute()

	rospy.spin()
	sis.stop()

if __name__ == '__main__':
	main()

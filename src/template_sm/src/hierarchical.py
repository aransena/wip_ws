#!/usr/bin/env python
import time
import random 
import rospy
import smach
import smach_ros

import states as states

##### main #####

def main():
	rospy.init_node('hierarchical')

	#smach state machine
	sm_top = smach.StateMachine(outcomes=['task_success', 'task_error'])#'task_fail', 'task_error'])

	#open container
	with sm_top:

		smach.StateMachine.add('S0', states.A(), transitions={'proceed':'S1', 'error':'ERR'})

		smach.StateMachine.add('S1', states.B(), transitions= {'proceed':'S2', 'error':'ERR', 'wait':'S1'})

		smach.StateMachine.add('S2', states.C(), transitions= {'success':'S3', 'error':'ERR'})
		

		hierarchical = smach.StateMachine(outcomes=['succeeded', 'failed'])

		with hierarchical:

			smach.StateMachine.add('Salpha', states.D(), transitions= {'success':'Sbeta', 'error':'failed'})

			smach.StateMachine.add('Sbeta', states.E(), transitions= {'success':'succeeded', 'error':'failed'})


		smach.StateMachine.add('S3', hierarchical, transitions={'succeeded':'S4_LOG', 'failed':'ERR'})

		smach.StateMachine.add('S4_LOG', states.log(), transitions= {'success':'S5_CLEANUP', 'error':'ERR'})

		smach.StateMachine.add('S5_CLEANUP',states.cleanup(), transitions= {'success_end':'task_success', 'error':'ERR'})#'fail_end':'task_fail', 'error':'ERR'}) 

		smach.StateMachine.add('ERR', states.error_handler(), transitions={'exit':'task_error'}) # error handling state
				
	sis = smach_ros.IntrospectionServer('server_name', sm_top, '/SM_HIERARCHICAL')
	sis.start()

	#execute SM
	outcome=sm_top.execute()
	print "result: ", outcome
	rospy.spin()
	sis.stop()

if __name__=='__main__':
	main()

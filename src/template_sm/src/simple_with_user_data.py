#!/usr/bin/env python
import time
import random 
import rospy
import smach
import smach_ros

import states_with_user_data as states # file with state information

## Example on state machine with data being passed between the states 

##### main #####

def main():
	rospy.init_node('FB1_state_machine')

	#smach state machine
	sm = smach.StateMachine(outcomes=['task_success', 'task_error'])#'task_fail', 'task_error'])

	#open container
	with sm:
		
		smach.StateMachine.add('S0', states.A(), transitions= {'proceed':'S1', 'error':'ERR'}, remapping= {'A_out':'sm_data'})

		smach.StateMachine.add('S1', states.B(), transitions= {'proceed':'S2', 'error':'ERR', 'wait':'S1'}, remapping= {'B_in':'sm_data', 'B_out':'sm_data'})

		smach.StateMachine.add('S2', states.C(), transitions= {'success':'S3', 'error':'ERR'})
		
		smach.StateMachine.add('S3', states.D(), transitions= {'success':'S4_LOG', 'error':'ERR'})

		smach.StateMachine.add('S4_LOG', states.log(), transitions= {'success':'S5_CLEANUP', 'error':'ERR'})

		smach.StateMachine.add('S5_CLEANUP',states.cleanup(), transitions= {'success_end':'task_success', 'error':'ERR'})#'fail_end':'task_fail', 'error':'ERR'}) 

		smach.StateMachine.add('ERR', states.error_handler(), transitions={'exit':'task_error'}) # error handling state
				
	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_SIMPLE_USER_DATA')
	sis.start()

	#execute SM
	outcome=sm.execute()
	print "result: ", outcome
	rospy.spin()
	sis.stop()

if __name__=='__main__':
	main()

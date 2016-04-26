#!/usr/bin/env python
import rospy
import smach
import smach_ros
import time

# Very simple state machine - generally a bad idea to put your 
# states in with your state machine. This would get messy quick
# as the program expands

class state1(smach.State):
	def __init__(self):
		smach.State.__init__(self,outcomes=['proceed'])

	def execute(self, userdata):
		rospy.loginfo('Executing S1')
                time.sleep(5)
		return 'proceed'

class state2(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['proceed'])

	def execute(self, userdata):
		rospy.loginfo('Executing S2')
                time.sleep(5)
		return 'proceed'


##### main #####

def smach_service_run():

	#smach state machine
	sm = smach.StateMachine(outcomes=['done'])

	#open container
	with sm:
		smach.StateMachine.add('S1', state1(), transitions={'proceed':'S2'})
		smach.StateMachine.add('S2', state2(), transitions={'proceed':'done'})
	
	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_SERVICE')
   	sis.start()
        
	#execute SM
	outcome=sm.execute()
	
    # we want to return the outcome for the purpose of calling the state machine externally
	return outcome

## Commented out as this file is being used for the ROS service/smach example

#if __name__=='__main__':
#	smach_service_run()

        

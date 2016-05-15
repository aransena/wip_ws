#!/usr/bin/env python
import random
import rospy
import smach
import smach_ros

from smach_ros import SimpleActionState
from smach_ros import ServiceState
from std_msgs.msg import String

import robot_router_states as states
import move_base_msgs.msg as MB


##### main #####

def run_FB2():
    # smach state machine
    rospy.init_node('smach_routing_state_machine')

    sm = smach.StateMachine(outcomes=['task_success', 'task_fail', 'task_error'])

    sm.userdata.sm_current_goal = MB.MoveBaseGoal()
    sm.userdata.sm_nav_goal = MB.MoveBaseGoal()
    sm.userdata.sm_request_goal = True
    sm.userdata.sm_intervention = False

    # open container
    with sm:
        smach.StateMachine.add('S0_INITALISE', states.initialise(),
                               transitions={'proceed': 'S1_READ', 'wait': 'S0_INITALISE', 'error': 'ERR'})
        smach.StateMachine.add('S1_READ', states.wait_for_control(),
                               transitions={'proceed': 'S2_SET_GOAL', 'error': 'ERR', 'finished': 'S5_CLEANUP','wait':'S1_READ'})
        smach.StateMachine.add('S2_SET_GOAL', states.set_goal(),
                               transitions={'new_goal': 'S3_NAVIGATE', 'error': 'ERR'},
                               remapping={'read_request_goal': 'sm_request_goal', 'send_nav_goal': 'sm_nav_goal'})
        smach.StateMachine.add('S3_NAVIGATE', states.navigate(),
                               transitions={'goal_reached': 'S1_READ', 'error': 'ERR', 'timeout': 'S1_READ', 'new_goal':'S2_SET_GOAL','intervention':'S3B_MONITOR'},
                               remapping={'read_nav_goal': 'sm_nav_goal', 'send_request_goal': 'sm_request_goal',
                                          'send_current_goal': 'sm_current_goal','intervention':'sm_intervention'})

        smach.StateMachine.add('S3B_MONITOR', states.monitor(),
                               transitions={'goal_reached': 'S1_READ', 'error': 'ERR', 'timeout': 'S1_READ', 'new_goal':'S1_READ','intervention':'S3B_MONITOR'},
                               remapping={'read_nav_goal': 'sm_nav_goal', 'send_request_goal': 'sm_request_goal',
                                          'send_current_goal': 'sm_current_goal','intervention':'sm_intervention'})

        smach.StateMachine.add('S5_CLEANUP', states.cleanup(),
                               transitions={'success_end': 'task_success', 'fail_end': 'task_fail', 'error': 'ERR'})
        smach.StateMachine.add('ERR', states.error_handler(),
                               transitions={'exit': 'task_error'})  # error handling state

    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_NAVIGATION_FB2')


    sis.start()  # execute SM
    outcome = sm.execute()

    return outcome

if __name__ == '__main__':
    run_FB2()

#!/usr/bin/env python
import time
import random
import math

import rospy
import smach
import smach_ros
# import threading
import actionlib
import subprocess

import tf

from move_base_msgs.msg import MoveBaseGoal
from move_base_msgs.msg import MoveBaseAction
from move_base_msgs.msg import MoveBaseActionFeedback

from smach_ros import SimpleActionState
from smach_ros import ServiceState
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped

responses = ['PENDING', 'ACTIVE', 'REJECTED', 'SUCCEEDED', 'ABORTED', 'PREEMPTING', 'PREEMPTED', 'RECALLING',
             'RECALLED', 'LOST']

global goal
stop = bool
benchmark_state = 0


# ----------- HELPER FUNCTIONS ---------#

def at_waypoint():
    print "..."
    # logcommand = "rosbag record -l 1 /chatter"
    #stopcommand = "rostopic pub /cmd_vel geometry_msgs/Twist '[0.0,0.0,0.0]' '[0.0,0.0,0.0]'"
    # subprocess.call([logcommand],shell=True)
    # subprocess.call([stopcommand],shell=True)
    # rospy.wait_for_service('roah_rsbb/end_execute')

    # try:
    # send_end = rospy.ServiceProxy('roah_rsbb/end_execute', SEND_END_COMMAND)
    #   	send_end()
    # except rospy.ServiceException, e:
    #    print "Service call failed: %s" % e


def callback_goal(data):
    #print data
    global goal
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'

    #goal.target_pose = data
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = data.x
    goal.target_pose.pose.position.y = data.y

    radians = math.radians(data.theta)
    quaternion = tf.transformations.quaternion_from_euler(0, 0, radians) # roll, pitch, yaw

    goal.target_pose.pose.orientation.x = quaternion[0]
    goal.target_pose.pose.orientation.y = quaternion[1]
    goal.target_pose.pose.orientation.z = quaternion[2]
    goal.target_pose.pose.orientation.w = quaternion[3]
    print goal  # goal = data



def callback_timeoutCheck(data):
    global timeout
    timeout = data


def callback_benchmark_state(data):
    global benchmark_state
    benchmark_state = data

def callback_curr_pos(data):
    #print data

    #pose = PoseWithCovarianceStamped()
    #pose = data

    #quaternion = (data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w)
    orientation = data.feedback.base_position.pose.orientation
    quaternion = (orientation.x,orientation.y,orientation.z,orientation.w)

    euler = tf.transformations.euler_from_quaternion(quaternion)
    #print math.degrees(euler[2])



# ----------- STATES---------#

class initialise(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['proceed', 'wait', 'error'])
        #rospy.Subscriber("roah_rsbb/benchmark/state")

    def execute(self, userdata):
        rospy.loginfo('Executing S0_INITIAL')
        try:
            #	rospy.wait_for_message("/roah_rsbb/benchmark/state", BenchmarkState, 5)
            #	if benchmark_state == BenchmarkState.PREPARE:
            return 'proceed'
        # else:
        #    return 'wait'

        except:
            print "PREPARE not received"


class wait_for_point(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['proceed', 'error', 'finished'])

    def execute(self, userdata):
        rospy.loginfo('Executing S1_READ')

        try:
            rospy.Subscriber("/nav_goal", Pose2D, callback_goal)
            rospy.wait_for_message("/nav_goal", Pose2D)
            return 'proceed'
        except Exception as e:
            print e
            print "no goal received"
            return 'error'


class set_goal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['new_goal', 'error'],
                             output_keys=['send_nav_goal'])
        global goal

    def execute(self, userdata):
        try:
            #print str(goal.x), str(goal.y), str(goal.theta)
            rospy.loginfo('Executing state S2_SET_GOAL')
            userdata.send_nav_goal = goal
            return 'new_goal'
        except Exception as e:
            print e
            return 'error'


class navigate(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['goal_reached', 'error', 'timeout', 'new_goal'],
                             input_keys=['read_nav_goal'],
                             output_keys=['send_request_goal', 'send_current_goal'])

        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    def execute(self, userdata):
        global goal
        rospy.loginfo('Executing state S3_NAVIGATE')
        # time.sleep(1)

        self.client.wait_for_server()

        #rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, callback_curr_pos)
        rospy.Subscriber("/move_base/feedback", MoveBaseActionFeedback, callback_curr_pos)

        # pub.publish(userdata.read_nav_goal)
        curr_nav_goal = userdata.read_nav_goal
        self.client.send_goal(curr_nav_goal)

        while (self.client.wait_for_result(rospy.Duration(1.0)) != True):
            print responses[self.client.get_state()]
            if curr_nav_goal != goal:
                print "NEW GOAL"
                self.client.cancel_all_goals()
                return 'new_goal'


        result = self.client.get_state()

        if result == 3:  ## success
            at_waypoint()
            return 'goal_reached'
        else:
            return 'error'


class cleanup(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success_end', 'fail_end', 'error'])

    def execute(self, userdata):
        rospy.loginfo('Executing state S5_CLEANUP')
        return 'success_end'
        # time.sleep(1)
        # if random.random() < 0.5:
        #    return 'success_end'
        # elif random.random() < 0.9:
        #    return 'fail_end'
        # else:
        #    return 'error'


class error_handler(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['exit'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ERR')
        time.sleep(1)
        return 'exit'

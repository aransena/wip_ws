#!/usr/bin/env python
import time
import math

import rospy
import smach
import actionlib

import tf

from move_base_msgs.msg import MoveBaseGoal
from move_base_msgs.msg import MoveBaseAction
from move_base_msgs.msg import MoveBaseActionFeedback
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose2D
from std_msgs.msg import String
from std_msgs.msg import Int8


import os
import json
dir = os.path.dirname(__file__)

responses = ['PENDING', 'ACTIVE', 'REJECTED', 'SUCCEEDED', 'ABORTED', 'PREEMPTING', 'PREEMPTED', 'RECALLING',
             'RECALLED', 'LOST']

MB_REJECTED = 2
MB_SUCCESS = 3
MB_ABORTED = 4


global goal
global curr_goal
global control_level
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
    print "RECEIVED GOAL" #goal  # goal = data


def callback_location(data):
    global goal
    goal = MoveBaseGoal()

    location_file = os.path.join(dir, 'locations/locations.json')
    locdata = json.loads(open(location_file).read())
    found = False
    for loc in locdata:
        if loc['Name'] == data.data:
            print "Found ", data.data
            print loc
            found=True
            location = loc
            break

    if found==True:
        #print data
        goal.target_pose.header.frame_id = 'map'

        #goal.target_pose = data
        goal.target_pose.header.stamp = rospy.Time.now()

        goal.target_pose.pose.position.x = location['X']
        goal.target_pose.pose.position.y = location['Y']

        radians = math.radians(location['Theta'])
        quaternion = tf.transformations.quaternion_from_euler(0, 0, radians) # roll, pitch, yaw

        goal.target_pose.pose.orientation.x = quaternion[0]
        goal.target_pose.pose.orientation.y = quaternion[1]
        goal.target_pose.pose.orientation.z = quaternion[2]
        goal.target_pose.pose.orientation.w = quaternion[3]
        print "LOCATION UPDATED"#goal  # goal = data

    else:
        goal = None



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

def callback_curr_goal(goal_data): # GOAL FROM RVIZ POINT UPDATE
    #print data

    #pose = PoseWithCovarianceStamped()
    #pose = data
    global curr_goal
    curr_goal = MoveBaseGoal()
    curr_goal.target_pose.header.frame_id = 'map'

    #goal.target_pose = data
    curr_goal.target_pose.header.stamp = rospy.Time.now()
    data = goal_data.pose
    curr_goal.target_pose.pose.position.x = data.position.x
    curr_goal.target_pose.pose.position.y = data.position.y

    curr_goal.target_pose.pose.orientation.x = data.orientation.x
    curr_goal.target_pose.pose.orientation.y = data.orientation.y
    curr_goal.target_pose.pose.orientation.z = data.orientation.z
    curr_goal.target_pose.pose.orientation.w = data.orientation.w

    #quaternion = (data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w)

    print "CURR GOAL UPDATED"#curr_goal

def callback_control_level(data):
    global control_level
    control_level = data.data


rospy.Subscriber("/move_base/feedback", MoveBaseActionFeedback, callback_curr_pos)
rospy.Subscriber("/move_base/current_goal", PoseStamped, callback_curr_goal)
rospy.Subscriber("/nav_goal", Pose2D, callback_goal)
rospy.Subscriber("/location_goal", String, callback_location)
rospy.Subscriber("/control_level", Int8, callback_control_level)

#rospy.Subscriber("/move_base/feedback", MoveBaseActionFeedback, callback_curr_pos)
#rospy.Subscriber("/move_base/current_goal", PoseStamped, callback_curr_goal)


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
            #rospy.Subscriber("/nav_goal", Pose2D, callback_goal)
            rospy.wait_for_message("/nav_goal", Pose2D)
            return 'proceed'
        except Exception as e:
            print e
            print "no goal received"
            return 'error'

class wait_for_location(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['proceed', 'error', 'finished'])

    def execute(self, userdata):
        rospy.loginfo('Executing S1_READ')

        try:
            #rospy.Subscriber("/location_goal", String, callback_location)
            rospy.wait_for_message("/location_goal", String)
            if goal is None:
                return 'error' # change to loop back on waiting
            else:
                return 'proceed'
        except Exception as e:
            print e
            print "no goal received"
            return 'error'

class wait_for_control(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['proceed','wait', 'error', 'finished'])

    def execute(self, userdata):
        rospy.loginfo('Executing S1_READ')

        try:
            #rospy.Subscriber("/location_goal", String, callback_location)
            rospy.wait_for_message("/control_level", Int8)
            if control_level < 1:
                return 'wait' # change to loop back on waiting
            else:
                if goal is None:
                    return 'error'
                else:
                    return 'proceed'
        except Exception as e:
            print e
            print "no control received"
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
        smach.State.__init__(self, outcomes=['goal_reached', 'error', 'timeout', 'new_goal','intervention'],
                             input_keys=['read_nav_goal'],
                             output_keys=['send_request_goal', 'send_current_goal','intervention'])

        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    def execute(self, userdata):
        global control_level
        global goal
        rospy.loginfo('Executing state S3_NAVIGATE')
        # time.sleep(1)

        self.client.wait_for_server()
        #rospy.Subscriber("/move_base/feedback", MoveBaseActionFeedback, callback_curr_pos)
        #rospy.Subscriber("/move_base/current_goal", PoseStamped, callback_curr_goal)
        curr_nav_goal = userdata.read_nav_goal
        self.client.send_goal(curr_nav_goal)

        while (self.client.wait_for_result(rospy.Duration(1.0)) != True):
            print responses[self.client.get_state()]
            if control_level < 1:
                self.client.cancel_all_goals()
                return 'goal_reached'

            elif curr_nav_goal != goal:
                print "NEW GOAL"
                self.client.cancel_all_goals()

                #return 'new_goal'


        result = self.client.get_state()


        if result == MB_SUCCESS:  ## success
            at_waypoint()
            return 'goal_reached'
        elif result == MB_ABORTED:
            return 'new_goal'
        elif result == MB_REJECTED:
            userdata.intervention=True
            #print userdata.intervention
            return 'intervention'
        else:
            return 'error'

class monitor(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['goal_reached', 'error', 'timeout', 'new_goal','intervention'],
                             input_keys=['read_nav_goal','intervention'],
                             output_keys=['send_request_goal', 'send_current_goal','intervention'])

        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    def execute(self, userdata):
        global goal
        global curr_goal
        global control_level

        rospy.loginfo('Executing state S3B_MONITOR')
        # time.sleep(1)
        #self.client.wait_for_server()

        self.client.wait_for_server()
        #rospy.Subscriber("/move_base/feedback", MoveBaseActionFeedback, callback_curr_pos)
        #rospy.Subscriber("/move_base/current_goal", PoseStamped, callback_curr_goal)
        #curr_nav_goal = userdata.read_nav_goal
        self.client.send_goal(curr_goal)

        goal = curr_goal

        while (self.client.wait_for_result(rospy.Duration(1.0)) != True):
            print responses[self.client.get_state()]
            if control_level < 1:
                self.client.cancel_all_goals()
                return 'goal_reached'
            elif curr_goal != goal:
                curr_goal = goal
                print "NEW GOAL"
                self.client.cancel_all_goals()

                #return 'new_goal'


        result = self.client.get_state()
        print "RESULT: ", result

        if result == MB_SUCCESS:  ## success
            at_waypoint()
            return 'goal_reached'
        elif result == MB_ABORTED:
            return 'new_goal'
        elif result == MB_REJECTED:
            userdata.intervention=True
            #print userdata.intervention
            return 'intervention'
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

#!/usr/bin/env python
import sys
import rospy
from std_srvs.srv import Empty

# Example on how to call a state machine as a service in rospy

def sm_serv_client():
	# wait for the service to become available
    rospy.wait_for_service('smach_service')

    try:
    	# define a service proxy, takes an empty input
        sm = rospy.ServiceProxy('smach_service', Empty)

        # call the service and get the response
        resp1 = sm()

        # return the response as an output from the function
        return resp1

    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    print sm_serv_client()


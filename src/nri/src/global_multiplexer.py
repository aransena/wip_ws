#!/usr/bin/env python

import rospy
import sys
import math
import time
import logging, threading, functools


from std_msgs.msg import String
from std_msgs.msg import Int8



active_device = 0

# from std_msgs.msg import Int8 as Int

def control_timeout():
    global active_device
    active_device = 0
    pub.publish(active_device)
    timer.cancel()
    print "Active device timeout"



class ControlTimeout(object):
    def __init__(self, interval, callback):
        self.interval = interval
        self.running = False
        self.thread = None

        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)
            if result:
                self.thread = threading.Timer(self.interval,
                                              self.callback)
                #self.thread.start()
        self.callback = wrapper
        #self.thread = threading.Timer(self.interval, self.callback)

    def start(self):

#        if self.running==False:
        print self.thread
        self.running = True
        if self.thread is None:
        #try:
            self.thread = threading.Timer(self.interval, self.callback)
            self.thread.start()
        #else:

        #    self.thread.start()
        print "Thread start"

    def cancel(self):
        self.running = False
        self.thread.cancel()
        self.thread = None
        print "Thread End"

    def alive(self):
        return self.running

def control_request(data):
    global active_device
    request_device = data.data
    print "CHECK: ",timer.alive()
    if timer.alive()==False:
        timer.start()
    #print "Request received: ",request_device, "Active: ", active_device
    if request_device>active_device:
        active_device= request_device
        print request_device, "set to current active device"
        #timer.cancel() # Cancel timeout, new device in control
        #timer.start() # Restart timeout check
    elif request_device==active_device:
        #pass
        timer.cancel() # Cancel timeout, current device active
        timer.start() # Restart timeout check
    else:
        print "Superceded by current active device, ", active_device
        # Timeout keeps running, active device or higher priority device yet to report in



    pub.publish(active_device)
    #rate.sleep()


if __name__ == "__main__":

    try:
        rospy.init_node('nri_multiplexer', anonymous=True)
        pub = rospy.Publisher('active_device', Int8, latch=True, queue_size=1)
        rospy.Subscriber("control_request", Int8, control_request)

        timer = ControlTimeout(5, control_timeout)
        #timer.start()
        print "HERE"

        rate = rospy.Rate(1) # 10hz
        rospy.spin()

    except rospy.ROSInterruptException:
        pass

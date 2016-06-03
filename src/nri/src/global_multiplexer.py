#!/usr/bin/env python

import rospy
import sys
import math
import time
import logging, threading, functools


from std_msgs.msg import String
from std_msgs.msg import Int8

active_device = 0

def control_timeout():
    global active_device
    active_device = 0
    pub.publish(active_device)
    timer.cancel()
    log_str = "Active device timeout"
    rospy.logwarn(log_str)

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
        self.callback = wrapper

    def start(self):
        self.running = True
        if self.thread is None:
            self.thread = threading.Timer(self.interval, self.callback)
            self.thread.start()


    def cancel(self):
        self.running = False
        self.thread.cancel()
        self.thread = None
        #print "Thread End"

    def alive(self):
        return self.running

def control_request(data):
    global active_device
    request_device = data.data

    if timer.alive()==False:
        timer.start()

    if request_device>active_device:
        active_device= request_device
        log_str = str(request_device) + " set to current active device"
        rospy.loginfo(log_str)

    elif request_device==active_device:
        #pass
        timer.cancel() # Cancel timeout, current device active
        timer.start() # Restart timeout check
    else:
        log_str = "Device " + str(request_device) + " superceded by current active device, " + "device " + str(active_device)
        rospy.loginfo(log_str)
        # Timeout keeps running, active device or higher priority device yet to report in



    pub.publish(active_device)
    rate.sleep()


if __name__ == "__main__":

    try:
        rospy.init_node('nri_multiplexer', anonymous=True)
        pub = rospy.Publisher('mux/active_device', Int8, latch=True, queue_size=1)
        rospy.Subscriber("mux/control_request", Int8, control_request)

        timer = ControlTimeout(5, control_timeout)
        rospy.loginfo("NRI Multiplexer Active")


        rate = rospy.Rate(100) # 10hz
        rospy.spin()

    except rospy.ROSInterruptException:
        pass

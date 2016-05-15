#!/usr/bin/env python

import rospy
import tf
import json

import os
dir = os.path.dirname(__file__)


from move_base_msgs.msg import MoveBaseActionFeedback
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D


def callback_location_delete(data):
    name = data.data
    print name

    location_file = os.path.join(dir, 'locations/locations.json')
    found = False
    try:
        jdata = json.loads(open(location_file).read())
        #file.write(dumps({'numbers':n, 'strings':s, 'x':x, 'y':y}, file, indent=4))
        with open(location_file, "w") as outfile:
            for l in jdata:
                if l['Name'] == name:
                    jdata.remove(l)
                    print "Deleted json"
                    found = True
                    break

            json.dump(jdata, outfile, indent=4)

        if found==True:
            print "Deleted location"
        else:
            print "Location not found"

    except Exception as e:
        print e
        pass


if __name__ == '__main__':
    try:

        rospy.Subscriber("/trigger_location_delete", String, callback_location_delete)  ###
        rospy.init_node('location_deleter', anonymous=True)

        rospy.spin()

    except Exception as e:
        print "Location Saver Error: ", e
        pass

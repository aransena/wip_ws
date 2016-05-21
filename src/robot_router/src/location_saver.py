#!/usr/bin/env python

import rospy
import tf
import json

import os
dir = os.path.dirname(__file__)
print dir


from move_base_msgs.msg import MoveBaseActionFeedback
from std_msgs.msg import String
from geometry_msgs.msg import Pose2D

global location

def callback_curr_pos(data):
    print "DATA: ", data
    global location
    location = Pose2D()
    position = data.feedback.base_position.pose.position
    location.x = position.x
    location.y = position.y
    orientation = data.feedback.base_position.pose.orientation
    quaternion = (orientation.x,orientation.y,orientation.z,orientation.w)

    euler = tf.transformations.euler_from_quaternion(quaternion)
    location.theta=euler[2]
    #print location.x, location.y, location.theta
    #print math.degrees(euler[2])


def callback_location_save(data):
    name = data.data
    global location
    #print name
    #print location
    msg = {"Name": name,"X": location.x,"Y": location.y,"Theta": location.theta}

    location_file = os.path.join(dir, 'locations/locations.json')

    try:
        jdata = json.loads(open(location_file).read())
        #file.write(dumps({'numbers':n, 'strings':s, 'x':x, 'y':y}, file, indent=4))
        with open(location_file, "w") as outfile:
            for l in jdata:
                if l['Name'] == msg['Name']:
                    jdata.remove(l)
                    print "Replaced in json"
                    break

            jdata.append(msg)
            json.dump(jdata, outfile, indent=4)

    except Exception as e:
        print e
        with open(location_file, "w") as outfile:
            json.dump([msg], outfile, indent=4)
        pass


    #f = open('/home/aransena/wip_ws/src/robot_router/locations/locations.json', 'r')

    #jdata = json.loads(open(location_file).read())
    #print jdata
    #print "Home" in jdata

    #    print "Home"==l['Name']
    #msg = [name,location.x,location.y,location.theta]

    #str_msg = str(msg)
    #f.write(str_msg)

if __name__ == '__main__':
    try:
        rospy.Subscriber("/move_base/feedback", MoveBaseActionFeedback, callback_curr_pos)
        rospy.Subscriber("/trigger_location_save", String, callback_location_save)  ###
        rospy.init_node('location_saver', anonymous=True)

        rospy.spin()

    except Exception as e:
        print "Location Saver Error: ", e
        pass

#!/usr/bin/env python

import rospy
import dynamic_reconfigure.client
from std_msgs.msg import Int8

def callback_config(config):
    print "Updated"#, config
    #rospy.loginfo("Config set to {int_param}, {double_param}, {str_param}, {bool_param}, {size}".format(**config))

def callback_control_change(data):
    control_level = data.data
    print "Data: ", control_level
    if control_level==3:
        client.update_configuration({"max_vel_x":0.5, "max_rot_vel":5.0, "min_rot_vel":0.4})
    elif control_level==2:
        client.update_configuration({"max_vel_x":0.3, "max_rot_vel":3.0, "min_rot_vel":0.4})
    elif control_level==1:
        client.update_configuration({"max_vel_x":0.2, "max_rot_vel":2.0, "min_rot_vel":0.4})
    else:
        client.update_configuration({"max_vel_x":0.0, "max_rot_vel":0.0, "min_rot_vel":0.0})


if __name__ == "__main__":
    try:
        client = dynamic_reconfigure.client.Client("/move_base/DWAPlannerROS", timeout=30, config_callback=callback_config)
        rospy.init_node("move_base_parameters_client")
        rospy.Subscriber("/control_level", Int8, callback_control_change)

        rospy.spin()
    except Exception as e:
        print "Move base parameter client error: ", e

    #r = rospy.Rate(0.1)
    #x = 0
    #b = False
    #while not rospy.is_shutdown():
    #   x = x+1
    #    if x>10:
    #        x=0
    #    b = not b
    #    client.update_configuration({"int_param":x, "double_param":(1/(x+1)), "str_param":str(rospy.get_rostime()), "bool_param":b, "size":1})
    #    r.sleep()

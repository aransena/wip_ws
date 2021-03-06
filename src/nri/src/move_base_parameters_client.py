#!/usr/bin/env python

import rospy
import dynamic_reconfigure.client
from std_msgs.msg import Int8

def callback_config(config):
    print "Updated"#, config


def callback_control_change(data):
    control_level = data.data
    print "Data: ", control_level
    try:
        
        if control_level==4 or control_level==1:
#        client.update_configuration({"max_vel_x":0.5, "max_rot_vel":5.0, "min_rot_vel":0.4})
            client.update_configuration({"max_vel_x":0.2, "max_vel_theta":1.0, "min_vel_theta":-1.0})
        elif control_level==3:
#        client.update_configuration({"max_vel_x":0.3, "max_rot_vel":3.0, "min_rot_vel":0.4})
            client.update_configuration({"max_vel_x":0.15, "max_vel_theta":0.8, "min_vel_theta":-0.8})
        elif control_level==2:
#        client.update_configuration({"max_vel_x":0.2, "max_rot_vel":2.0, "min_rot_vel":0.4})
            client.update_configuration({"max_vel_x":0.1, "max_vel_theta":0.6, "min_vel_theta":-0.6})
        else:
            client.update_configuration({"max_vel_x":0.0, "max_vel_theta":0.0, "min_vel_theta":0.0})
    except Exception as e:
	print "Param client error: ", e

if __name__ == "__main__":
    try:
	client = dynamic_reconfigure.client.Client("/move_base/TrajectoryPlannerROS", timeout=30, config_callback=callback_config)
        rospy.init_node("move_base_parameters_client")
        rospy.Subscriber("/nri_system/control_level", Int8, callback_control_change)

        rospy.spin()
    except Exception as e:
        print "Move base parameter client error: ", e


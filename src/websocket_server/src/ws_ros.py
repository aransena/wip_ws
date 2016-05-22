#!/usr/bin/env python

# sample code from http://iot-projects.com/index.php?id=websocket-a-simple-example

import rospy
from std_msgs.msg import String as ros_string
from std_msgs.msg import Float64 as ros_float

from geometry_msgs.msg import Twist

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import json

# pub = rospy.Publisher('websocket_server_msgs', ros_string)
outfile = open('data.txt', 'w')
global heading
global tilt


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print 'user is connected.\n'

    def on_message(self, message):
        global tilt
        #print "Message: ", message

        if "LOCATION" in message:
            loc = message.split(",")[1]
            #print "GOTO: ", loc
            loc_pub.publish(loc)
        elif "UPDATE" in message:
            loc = message.split(",")[1]
            #print "UPDATE: ", loc
            loc_update_pub.publish(loc)
        elif len(message) > 10:
            try:
                msg = json.loads(message)
                json.dump(msg, outfile)
                pub.publish(str(message))
            except:
                msg=""
                pass

            try:
                device = msg['Device']
                if device == "SmartWatch":
                    global heading
                    try:
                        heading_msg = {u"heading": heading}
                    except Exception, e:
                        print "Error setting heading message: ", e
                        pass
                    self.write_message(json.dumps(heading_msg))
            except Exception, e:

                print "Error sending heading to watch: ", e
                pass

        # print 'received message: %s\n' % json.loads(message)

        elif message == "USER":
            print "Responding..."
            self.write_message(message)  # + ' OK')

        elif message == "TILT_UP":
            if tilt + 10 > -15:
                send_tilt = -15
            else:
                send_tilt = tilt + 10

            kinect_pub.publish(send_tilt)

        elif message == "TILT_DOWN":
            if tilt - 10 < -60:
                send_tilt = -60
            else:
                send_tilt = tilt - 10

            kinect_pub.publish(send_tilt)



def on_close(self):
    print 'connection closed\n'


application = tornado.web.Application([(r'/ws', WSHandler), ])


def twist_listener(cmd_msg):
    global heading
    heading = cmd_msg.angular.z


def tilt_angle_listener(angle):
    global tilt
    if angle.data != 64:
        tilt = angle.data


if __name__ == "__main__":
    try:
        global heading
        heading = 0

        rospy.init_node('websocket_server', anonymous=True)

        pub = rospy.Publisher('websocket_server_msgs', ros_string, queue_size=1)
        loc_pub = rospy.Publisher('location_goal', ros_string, queue_size=1)
        loc_update_pub = rospy.Publisher('trigger_location_save', ros_string, queue_size=1)
        kinect_pub = rospy.Publisher('tilt_angle', ros_float, queue_size=1)
        rospy.Subscriber("/smooth_cmd_vel", Twist, twist_listener)  ### CHANGE TO SMOOTH_CMD_VEL
        #rospy.Subscriber('/cmd_vel_mux/input/teleop', Twist, twist_listener)  ### CHANGE TO SMOOTH_CMD_VEL
        rospy.Subscriber("/cur_tilt_angle", ros_float, tilt_angle_listener)  ###

        rospy.loginfo("Websocket server started")

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()


    except Exception, e:
        print "Server Error ", e
        pass

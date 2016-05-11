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

pub = rospy.Publisher('websocket_server_msgs', ros_string)
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
        print message
        if len(message) > 10:
            try:
                msg = json.loads(message)
                json.dump(msg, outfile)
            except:
                message = ""
                pass
        # print 'received message: %s\n' % json.loads(message)
        pub.publish(str(message))
        if message == "USER":
            print "Responding..."
            self.write_message(message)  # + ' OK')

        elif message == "TILT_UP":
            kinect_pub.publish(tilt + 10)
        elif message == "TILT_DOWN":
            kinect_pub.publish(tilt - 10)

        else:
            try:
                device = msg['Device']
                if device == "SmartWatch":
                    global heading
                    try:
                        heading_msg = {u"heading": heading}
                    except Exception, e:
                        print e
                        pass
                    self.write_message(json.dumps(heading_msg))
            except Exception, e:
                print e
                pass


def on_close(self):
    print 'connection closed\n'


application = tornado.web.Application([(r'/ws', WSHandler), ])


def twist_listener(cmd_msg):
    global heading
    heading = cmd_msg.angular.z


def tilt_angle_listener(angle):
    global tilt
    tilt = angle.data
    print tilt


if __name__ == "__main__":
    try:
        global heading
        heading = 0

        pub = rospy.Publisher('websocket_server_msgs', ros_string)
        kinect_pub = rospy.Publisher('tilt_angle', ros_float)
        rospy.Subscriber("/smooth_cmd_vel", Twist, twist_listener)  ### CHANGE TO SMOOTH_CMD_VEL
        rospy.Subscriber("/cur_tilt_angle", ros_float, tilt_angle_listener)  ###
        rospy.init_node('websocket_server', anonymous=True)
        rospy.loginfo("websocket_server started")

        http_server = tornado.httpserver.HTTPServer(application)
        try:
            print(2)
            # http_server.close_all_connections()
            print(3)
        except:
            pass
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

    except Exception, e:
        print "Server Error ", e
        pass

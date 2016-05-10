#!/usr/bin/env python

# sample code from http://iot-projects.com/index.php?id=websocket-a-simple-example

import rospy
from std_msgs.msg import String as ros_string

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import json

pub = rospy.Publisher('websocket_server_msgs', ros_string)
outfile = open('data.txt', 'w')
class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print 'user is connected.\n'

    def on_message(self, message):
        print message
        if len(message) > 10:
            msg = json.loads(message)
            json.dump(msg, outfile)
        #print 'received message: %s\n' % json.loads(message)
        pub.publish(str(message))
        if message == "USER":
            print "Responding..."
            self.write_message(message)  # + ' OK')

    def on_close(self):
        print 'connection closed\n'


application = tornado.web.Application([(r'/ws', WSHandler), ])

if __name__ == "__main__":
    try:
        pub = rospy.Publisher('websocket_server_msgs', ros_string)
        rospy.init_node('websocket_server', anonymous=True)
        rospy.loginfo("websocket_server started")

        http_server = tornado.httpserver.HTTPServer(application)
        try:
            print(2)
            #http_server.close_all_connections()
            print(3)
        except:
            pass
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

    except Exception,e:
        print "Server Error ", e
        pass


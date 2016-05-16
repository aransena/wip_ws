#!/usr/bin/env python
import rosbag
from geometry_msgs.msg import PoseWithCovarianceStamped
#from nav_msgs.msg import OccupancyGrid
import matplotlib.pyplot as plt
import numpy as np
#import os
#from scipy.misc import imread

#dir = os.path.expanduser("~")
#print "DIR: ", dir
#map_file = os.path.join(dir, 'wip_ws/src/robot_2dnav/maps/map.pgm')
#map_file = os.path.join(dir,'/opt/ros/indigo/share/turtlebot_gazebo/maps/playground.pgm')
bag = rosbag.Bag('test.bag')
print bag
X=[]
Y=[]
#map = OccupancyGrid()
firstRun = True

x = 0
y = 0
x_prev = 0
y_prev = 0
dist_tot = 0

for topic, msg, t in rosbag.Bag('test.bag').read_messages():
#for topic, msg, t in bag.read_messages(topics=['amcl_pose']):
    #if topic =="/map":
    #    map = msg

    if topic == "/amcl_pose":#print topic
        point = PoseWithCovarianceStamped()
        point = msg
        x = point.pose.pose.position.x
        y = point.pose.pose.position.y
        if(firstRun==True):
            x_prev = x
            y_prev = y
            firstRun = False
        X.append(x)
        Y.append(y)
        dist_tot = dist_tot + np.sqrt(np.power((x-x_prev),2)+np.power((y-y_prev),2))
        x_prev = x
        y_prev = y

bag.close()

print dist_tot
#X = X*1000
#Y = Y*1000

#img = imread(map_file)

plt.figure(1)

#plt.imshow(img,zorder=0,origin=)
plt.plot(X,Y)
plt.show()

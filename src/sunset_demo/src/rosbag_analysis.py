#!/usr/bin/env python
import rosbag
from geometry_msgs.msg import PoseWithCovarianceStamped
#from nav_msgs.msg import OccupancyGrid
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.misc import imread

dir = os.path.expanduser("~")
print "DIR: ", dir
#map_file = os.path.join(dir, 'wip_ws/src/robot_2dnav/maps/map.pgm')
map_file = os.path.join(dir,'/opt/ros/indigo/share/turtlebot_gazebo/maps/playground.pgm')
map_yaml = os.path.join(dir,'/opt/ros/indigo/share/turtlebot_gazebo/maps/playground.yaml')

origin_offset_x = 0
origin_offset_y = 0
map_scale = 0
print "\n---------------\n"
f = open(map_yaml,'r')
for line in f:
    if "origin" in line:
        origin_offset_x = float(line.split()[1][1:-1])
        origin_offset_y = float(line.split()[2][:-1])
        print "offsets: ", origin_offset_x, " ", origin_offset_y

    if "resolution" in line:
        map_scale = float(line.split()[1])
        print "map scale: ", (1/map_scale)

f.close()

bag = rosbag.Bag('test.bag')
print "\n---------------\n"
print bag
print "\n---------------\n"
X=[]
Y=[]
#map = OccupancyGrid()
firstRun = True

x = 0
y = 0
x_prev = 0
y_prev = 0
dist_tot = 0
#origin_offset_x = -6.89999
#origin_offset_y = -5.89999

for topic, msg, t in rosbag.Bag('test.bag').read_messages():
#for topic, msg, t in bag.read_messages(topics=['amcl_pose']):
    #if topic =="/map":
    #    map = msg

    if topic == "/amcl_pose":#print topic
        point = PoseWithCovarianceStamped()
        point = msg
        x = (point.pose.pose.position.x - origin_offset_x)*(1/map_scale)
        y = (point.pose.pose.position.y - origin_offset_y)*(1/map_scale)
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

print "Distance travelled: ", round(dist_tot*map_scale, 2),"m"
#X = X*1000
#Y = Y*1000

img = imread(map_file)


plt.figure(1)
img =np.flipud(img)
y1=img.shape[0]
x1=img.shape[1]
plt.imshow(img,zorder=0,origin='lower', extent=[0,x1,0,y1],cmap=plt.cm.gray)
plt.plot(X,Y)
plt.show()

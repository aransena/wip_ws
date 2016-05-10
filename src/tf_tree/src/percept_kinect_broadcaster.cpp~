#include <ros/ros.h>
#include <tf/transform_broadcaster.h> // from ROS Indigo shared
#include "std_msgs/Float32.h"


int main(int argc, char** argv){

	ros::init(argc, argv, "percept_kinect_publisher_tf");
	ros::NodeHandle n;

	ros::Rate r(10);

	tf::TransformBroadcaster broadcaster;
	
//	printf("%.2d \n",rand()%100);
	while(n.ok()){

	//	float z = rand()%100; 									// variable z axis for platform - replace with subscription to a topic?
		broadcaster.sendTransform(
			tf::StampedTransform(
				tf::Transform(tf::Quaternion(0,0,0,1),  		//transform does not need to rotate the sensor
					tf::Vector3(0.23,0.0,0.96)),					//trasform DOES need to translate the sensor (x,y,z)
				ros::Time::now(),"hip_link", "percept_kinect_link"));
				//printf("okay\n");
		r.sleep();
	}
}
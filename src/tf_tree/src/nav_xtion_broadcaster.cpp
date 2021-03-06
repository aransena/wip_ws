#include <ros/ros.h>
#include <tf/transform_broadcaster.h> // from ROS Indigo shared
#include "std_msgs/Float32.h"

int main(int argc, char** argv){

	ros::init(argc, argv, "tf/nav_xtion_publisher_tf");
	ros::NodeHandle n;

	ros::Rate r(50);

	tf::TransformBroadcaster broadcaster;
//	printf("%.2d \n",rand()%100);
	while(n.ok()){
		
	//	float z = rand()%100; 									// variable z axis for platform - replace with subscription to a topic?
		broadcaster.sendTransform(
			tf::StampedTransform(
				tf::Transform(tf::Quaternion(0.1,0,0,0),  		//transform does not need to rotate the sensor
					tf::Vector3(0.385,0.00,0.047)),					//trasform DOES need to translate the sensor (x,y,z)

				ros::Time::now(),"base_link", "xtion_link"));
				//printf("okay\n");
		r.sleep();
	}
}

#include <ros/ros.h>
#include <tf/transform_broadcaster.h> // from ROS Indigo shared
#include "std_msgs/Float32.h"

float z;

void chatterCallback(const std_msgs::Float32::ConstPtr& msg);

int main(int argc, char** argv){

	ros::init(argc, argv, "laser_publisher_tf");
	ros::NodeHandle n;

	ros::Rate r(10);

	tf::TransformBroadcaster broadcaster;
	
	ros::Subscriber sub = n.subscribe("z_axis_chatter",100,chatterCallback);

	while(n.ok()){

		broadcaster.sendTransform(
			tf::StampedTransform(
				tf::Transform(tf::Quaternion(1,0,0,0),  		//transform does not need to rotate the sensor
					tf::Vector3(0.195,0.0,z-0.075)),					//trasform DOES need to translate the sensor (x,y,z)
//				ros::Time::now(),"hip_link", "laser"));

				ros::Time::now(),"shoulder_link", "laser"));

				//printf("okay\n");
		r.sleep();
	}
}

void chatterCallback(const std_msgs::Float32::ConstPtr& msg){
	z = msg->data;
	//printf("z: %.2f \n",z);
}

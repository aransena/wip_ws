#include <ros/ros.h>
#include <tf/transform_broadcaster.h> // from ROS Indigo shared
#include "std_msgs/Float32.h"

float x_pos;
float y_pos;
float omega_orient;

void chatterCallback(const std_msgs::Float32::ConstPtr& msg);

int main(int argc, char** argv){

	ros::init(argc, argv, "new_global_publisher_tf");
	ros::NodeHandle n;

	ros::Rate r(10);

	tf::TransformBroadcaster broadcaster;
	
//	printf("%.2d \n",rand()%100);
	x_pos = 0.0;
	y_pos = 0.0;
	omega_orient = 0.0;
	ros::Subscriber sub = n.subscribe("z_axis_chatter",100,chatterCallback);
	while(n.ok()){
		ros::spinOnce();

	//	float z = rand()%100; 									// variable z axis for platform - replace with subscription to a topic?
		broadcaster.sendTransform(
			tf::StampedTransform(
				tf::Transform(tf::Quaternion(0,0,omega_orient,1),  		//transform does not need to rotate the sensor
					tf::Vector3(x_pos,y_pos,0)),					//trasform DOES need to translate the sensor (x,y,z)
				ros::Time::now(),"odom", "new_global_link"));
				//printf("okay\n");
		r.sleep();
	}
}

void chatterCallback(const std_msgs::Float32::ConstPtr& msg){
	x_pos = msg->data;
	y_pos = msg->data;
	omega_orient = msg->data;	//printf("z: %.2f \n",z);
}
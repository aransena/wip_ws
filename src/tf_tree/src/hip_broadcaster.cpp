#include <ros/ros.h>
#include <tf/transform_broadcaster.h> // from ROS Indigo shared
#include "std_msgs/Float32.h"
#include "geometry_msgs/Quaternion.h"
//#include <ros/console.h>
//#include <math.h>
//float theta;

//void chatterCallback(const std_msgs::Float32::ConstPtr& msg);

int main(int argc, char** argv){

	ros::init(argc, argv, "hip_publisher_tf");
	ros::NodeHandle n;

	ros::Rate r(10);

	tf::TransformBroadcaster broadcaster;
	
//	printf("%.2d \n",rand()%100);
	//ros::Subscriber sub = n.subscribe("z_axis_chatter",100,chatterCallback);
	int theta = 0.0;
	while(n.ok()){
		//ros::spinOnce();
		geometry_msgs::Quaternion quaternion;
		quaternion.x = 0;
		quaternion.y = 0;
		quaternion.z = sin(theta/2.0);
		quaternion.w = cos(theta/2.0);

		printf("z: %f \n", quaternion.z);
		printf("w: %f \n", quaternion.w);
		broadcaster.sendTransform(
			tf::StampedTransform(
				tf::Transform(tf::Quaternion(0,0,quaternion.z,quaternion.w),  		//transform does not need to rotate the sensor
					tf::Vector3(0.148,0.0,0.2795)),					//trasform DOES need to translate the sensor (x,y,z)
				ros::Time::now(),"base_link", "hip_link"));
				//printf("okay\n");
		r.sleep();
	}
}

/*void chatterCallback(const std_msgs::Float32::ConstPtr& msg){
	theta = msg->data;
	//printf("z: %.2f \n",z);
}*/
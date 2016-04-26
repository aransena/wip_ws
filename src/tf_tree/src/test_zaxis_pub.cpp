#include "ros/ros.h"
#include "std_msgs/Float32.h"

#include <sstream>

int main(int argc, char** argv){

	ros::init(argc,argv,"z_axis_talker");
	ros::NodeHandle n;

	ros::Publisher chatter_pub = n.advertise<std_msgs::Float32>("z_axis_chatter",1000);
	ros::Rate loop_rate(10);

	while(ros::ok()){
		std_msgs::Float32 msg;

		msg.data = 0.133;//rand()%100;

		//printf("z: %.2f \n",msg.data);

		chatter_pub.publish(msg);
		ros::spinOnce();

		loop_rate.sleep();
	}
}

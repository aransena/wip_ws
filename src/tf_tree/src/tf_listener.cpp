#include <ros/ros.h>
#include <geometry_msgs/PointStamped.h>
#include <tf/transform_listener.h> // from ROS Indigo shared


void transformPoint(const tf::TransformListener& listener);

int main(int argc, char** argv){

	ros::init(argc,argv,"tf_listener");
	ros::NodeHandle n;

	tf::TransformListener listener(ros::Duration(10));

	// transform point once per second
	// binding converts function call into an object which returns the value of the function call
	// binding is done so that the function call can be passed as an arg to n.createTimer
	ros::Timer time = n.createTimer(ros::Duration(1.0), boost::bind(&transformPoint, boost::ref(listener)));

	ros::spin();
}

////////////////////////////////////////////////////////////

void transformPoint(const tf::TransformListener& listener){
	
	geometry_msgs::PointStamped hip_point;
	
	hip_point.header.frame_id = "hip_link";

	hip_point.header.stamp = ros::Time();

	// stand in fixed point
	hip_point.point.x = 1.0;
	hip_point.point.y = 0.2;
	hip_point.point.z = 0.0;

	try{
		geometry_msgs::PointStamped base_point;
		listener.transformPoint("base_link", hip_point, base_point);

		//ROS_INFO("hip_link: (%.2f, %.2f, %.2f) -------> base_link: (%.2f, %.2f, %.2f) at time %.2f",
		//	hip_point.point.x, hip_point.point.y, hip_point.point.z,
		//	base_point.point.x, base_point.point.y, base_point.point.z, base_point.header.stamp.toSec());
	}

	catch(tf::TransformException& ex){
		ROS_ERROR("Received an exception trying to transform a point from \"hip_link\" to \"base_link\": %s", ex.what());
	}
}
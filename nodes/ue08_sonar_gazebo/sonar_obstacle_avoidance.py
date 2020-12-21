#!/usr/bin/env python3
# sonar_obstacle_avoidance.py
# ################################################################################
# edited WHS, OJ , 17.12.2020 #
# usage
# copy content of turtlebot3.burger.gazebo_sonar.xacro
#              to turtlebot3.burger.gazebo_sonar.xacro
# copy content of turtlebot3.burger.urdf_sonar.xacro
#              to turtlebot3.burger.urdf.xacro
#
#   $1 roslaunch rtc turtlebot3_action_server_client_path_gazebo_house.launch
#   $2 roslaunch turtlebot3_navigation turtlebot3_navigation.launch
#                map_file:=$HOME/catkin_ws/src/rtc/rtc_maps/gazebo_house_map_2020_12_07.yaml
#   $4 rosrun rtc turtlebot3_sonar.py
# ---------------------------------------

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range


class Sonar():
    def __init__(self):
        rospy.loginfo("Publishing sonar/cmd_vel")
        self.cmd_pub = rospy.Publisher('sonar/cmd_vel',
                                       Twist, queue_size=10)
        self.sonar_sub = rospy.Subscriber('sonar',
                                          Range,
                                          self.get_sonar,
                                          queue_size=10)
        self.rate = rospy.Rate(100)
        while not rospy.is_shutdown():
            self.rate.sleep()

    def get_sonar(self, sensor_data):
        # rospy.loginfo(" Sonar Data received ")
        twist = Twist()
        self.set_backward = True
        if sensor_data.range < 0.3:  # Hinderniss erkannt
            rospy.loginfo("Detected Obstacle in "
                          + str(sensor_data.range)
                          + " m Distance \a")  # Beep
            # zuruecksetzen und drehen
            turn_vel = -0.5
            lin_vel = -0.1
            twist.linear.x = lin_vel
            twist.angular.z = turn_vel
            self.cmd_pub.publish(twist)
            self.set_backward = True
        else:
            if sensor_data.range < 0.7 and self.set_backward:
                # zuruecksetzen und drehen
                turn_vel = 0.5
                lin_vel = -0.1
                twist.linear.x = lin_vel
                twist.angular.z = turn_vel
                self.cmd_pub.publish(twist)

                rospy.loginfo("Detected Obstacle in "
                              + str(sensor_data.range)
                              + " m Distance")
                rospy.loginfo("Robot goes backward ")
            else:
                rospy.loginfo("No Obstacle detected ")
            # nix senden


if __name__ == '__main__':
    rospy.init_node('sonar_controller', anonymous=True)
    try:
        sonar = Sonar()
    except rospy.ROSInterruptException:
        pass

#! /usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

class position_controller:

    def __init__(self, velocity_topic, odom_topic, gains):

        # params we'll need:
        # angular_Kp, angular_Ki, angular_Kd
        # lin_Kp, lin_Ki, lin_Kd

        self.ang_Kp,self.ang_Ki,self.ang_Kd = gains[0:3]
        self.lin_Kp,self.lin_Ki,self.lin_Kd = gains[3:6]

        rospy.init_node('position_controller')
        self.vel_pub = rospy.Publisher(velocity_topic, Twist, queue_size=1)
        self.odom_sub = rospy.Subscriber(odom_topic, Odometry, odom_callback)
        rospy.loginfo('node setup complete')

    def set_goal(self,x,y):
        self.goal_x = x
        self.goal_y = y
        self.lin_EA = 0
        self.lin_ED = 0
        self.ang_EA = 0
        self.ang_ED = 0

    def odom_callback(self, odom_msg):

        current_x = odom_msg.pose.pose.position.x
        current_y = odom_msg.pose.pose.position.y
        quat = odom_msg.pose.pose.orientation
        _, _, current_yaw = euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])

        # find errors
        Ex = current_x - self.goal_x
        Ey = current_y - self.goal_y
        Ea = math.atan2(self.goal_y, self.goal_x) - current_yaw

        
        

#!/usr/bin/env python

""" projenin iletisim kisiminida OOP olarak kodladım. 
 Ancak bu kod bir kaç kez çalışıp duruyor sebebini öğrenmek için zamanım yeterli olmadı.."""

import rospy

from grid_map_msgs.msg import GridMap
from std_msgs.msg import Float32MultiArray 
import numpy as np
#from nav_msgs.msg import OccupancyGrid
import math
from astar import *

class mapCommunicate:
    def __init__(self,initial_point,end_point):
        
        self.map_pub = rospy.Publisher('/image_to_gridmap_demo/grid_map', GridMap, queue_size=2)  
        
        self.initial_point=initial_point
        self.end_point=end_point
        self.maze_array=[]
        self.input_list=[]
        self.path=[]
        self.sub=rospy.Subscriber("/image_to_gridmap_demo/grid_map", GridMap, self.callback)
        


    def discritizer(self):
        for i in range(0, len(self.maze_array)):
            if  math.isnan(self.maze_array[i]) :
                self.maze_array[i] = 0
            else:
                self.maze_array[i] = 1

    def astarTransform(self): 
        init = 0 
        temp_list = []  
        for i in range(0, len(self.maze_array)+1):
            if i % self.row == 0 and i != 0:
                for j in range(init, i):
                    temp_list.append(self.maze_array[j])
                init = i
                self.input_list.append(temp_list)
                temp_list = []

    def collectData(self,data):
        self.row=data.data[0].layout.dim[0].size
        self.column=data.data[0].layout.dim[1].size
        self.maze_array=list(data.data[0].data)

    def callback(self,data):
        
        self.collectData(data)
        rospy.loginfo("hello_str1")
        self.discritizer()
        rospy.loginfo("hello_str2")
        self.astarTransform()
        
        rospy.loginfo(self.path)

        self.path = astar(self.input_list, self.initial_point, self.end_point)
        if  self.path is not None and self.path is not []:
            for i in self.path:
                r=i[0]
                c=i[1]
                self.input_list[r][c]=0.5
            templist=[]
            for j in self.input_list:
                templist+=j
        
            data.data[0].data=templist
            
            self.map_pub.publish(data)




if __name__ == '__main__':
    
    rospy.init_node('listener', anonymous=True)
    app = mapCommunicate((0,0),(1,1))
    rospy.Timer(rospy.Duration(2), app.__init__((0,0),(1,1)))
    try:
        rospy.spin()
        
    except KeyboardInterrupt:
        print("Shutting down")


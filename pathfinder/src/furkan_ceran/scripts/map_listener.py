#!/usr/bin/env python
import rospy

from grid_map_msgs.msg import GridMap
from std_msgs.msg import Float32MultiArray 
import numpy as np
#from nav_msgs.msg import OccupancyGrid
import math
from astar import *



def discritizer(maze_array):

    for i in range(0, len(maze_array)):
            if  math.isnan(maze_array[i]) :
                maze_array[i] = 0
            else:
                maze_array[i] = 1
    return maze_array
def astarTransform(row,column,maze_array):

    input_list=[]
    temp_list = []
    init = 0
    
    for i in range(0, len(maze_array)+1):
        if i % row == 0 and i != 0:
            for j in range(init, i):
                temp_list.append(maze_array[j])
            init = i
            
            input_list.append(temp_list)
            temp_list = []
    return input_list

def collectData(data):
    row=data[0].layout.dim[0].size
    column=data[0].layout.dim[1].size
    maze_array=list(data[0].data)
    return row,column,maze_array




def callback(data):

    row,column,maze_array=collectData(data.data)

    maze_array=discritizer(maze_array)
    input_list =astarTransform(row,column,maze_array)

    
    maze_array=data.data[0].data

    path = astar(input_list, start, end)
    
    if  path is not None:
        for i in path:
            r=i[0]
            c=i[1]
            input_list[r][c]=0.5
        templist=[]
        for j in input_list:
            templist+=j

        map_pub = rospy.Publisher('/image_to_gridmap_demo/grid_map', GridMap, queue_size=2)   
        data.data[0].data=templist


        rospy.loginfo("Solved!: "+str(path))
        map_pub.publish(data)






def listener():
    init_X=int(input("Please provide initial x location = "))
    init_Y=int(input("Please provide initial y location = "))
    
    end_X=int(input("Please provide end x location = "))
    end_Y=int(input("Please provide end y location = "))
    output= ("Calculating shortest path with A* algorithm at ({},{}) to ({},{}) points...")
    output=output.format(init_X,init_Y,end_X,end_Y)
    print(output)
    global start,end
    start = (init_X, init_Y)
    end = (end_X, end_Y)

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/image_to_gridmap_demo/grid_map", GridMap, callback)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()

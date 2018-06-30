#coding=utf-8
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
#import scipy.signal as sg


xx = np.arange(0, 10000)

smoothing_range = 10

average_buf = np.arange(0, smoothing_range)
ave_index = 0
ave_status = 0
width_count = 0
ave_sum = 0



peak_index = 0
peak_type = False
peak_first = 0
peak_min = 100
peak_max = 0

def calculate_peak(n):
    global peak_index,peak_first,peak_min,peak_max,peak_type

    if peak_min > n:
        peak_min = n
    if peak_max < n:
        peak_max = n

    if peak_index == 0:
        peak_first = n
        if peak_first < 0:
            peak_type = False
        else:
            peak_type = True
        peak_index += 1

    if peak_type == False and n < 0:
        retval = 0
    elif peak_type == True and n > 0:
        retval = 0
    else:
        if peak_type == False:
            if peak_min > -16 :
                peak_min = 0
            retval = peak_min
            peak_type = True
        else:
            if peak_max < 16:
                peak_max = 0
            retval = peak_max
            peak_type = False
        peak_min = 100
        peak_max = 0
    return retval


def calculate_average(n):
    global ave_sum, ave_index, ave_status
    ave_sum -= average_buf[ave_index]
    average_buf[ave_index] = n
    ave_sum += average_buf[ave_index]
    ave_index += 1
    if(ave_index == smoothing_range):
        ave_index = 0
        ave_status = 1
    if(ave_status == 1):
        ret_val = ave_sum / smoothing_range
    else :
        ret_val = 0
    return ret_val


base_number = 0
up_number = 0
down_number = 0
max_number = -127
min_number = 127

show_max = 0
show_min = 0

tendency_number = 5

def calculate_pole(n):
    global base_number, up_number, down_number, max_number, min_number, show_max, show_min
    ret_val = 0
    if(n > max_number):
        max_number = n
    if(n < min_number):
        min_number = n

    if(n > base_number):
        up_number += 1
        down_number = 0
        if(up_number > tendency_number and show_min == 0) :
            if(min_number < -46):
                ret_val = min_number
            min_number = 127
            show_min = 1
            show_max = 0
            down_number = 0
    elif(n < base_number):
        down_number += 1
        up_number = 0
        if(down_number > tendency_number and show_max == 0):
            #ret_val = max_number
            max_number = -127
            show_max = 1
            show_min = 0
            up_number = 0
    base_number = n
    return ret_val


#rootdir = 'E:\\400-8g'
rootdir = 'G:\\algo'
list = os.listdir(rootdir)
for j in range(0,len(list)):
    path = os.path.join(rootdir,list[j])
    if os.path.isfile(path) :
        f = open(path)
        #print "----------------------------------------------" + path
        base_number = 0
        up_number = 0
        down_number = 0
        max_number = -127
        min_number = 127

        show_max = 0
        show_min = 0

        xy = np.arange(0, 10000)
        yy = np.arange(0, 10000)
        zy = np.arange(0, 10000)
        bb = np.arange(0, 10000)
        i = 0
        while (i < 10000):
            xy[i] = 0
            yy[i] = 0
            zy[i] = 0
            bb[i] = 0
            i += 1
        line = f.readline()
        index = 0
        index2 = 0
        while index < 10000 and line:
            str = line.split(',')
            if (int(str[2]) == -1) and (int(str[1]) == -1) and (int(str[0]) == -1):
                break
            zy[index] = (int(str[0]))
            yy[index] = (int(str[1]))
            bb[index] = (int(str[2]))
            index += 1
            line = f.readline()
        #zz = sg.medfilt(zy, 49)
        plt.figure()
        plt.plot(xx, zy, label="$x$",color='g')
        plt.plot(xx, yy, 'r',label="$y$")
        plt.plot(xx, bb, 'b', label="$z$")
        plt.legend()
        plt.show()
        f.close()













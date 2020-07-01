import matplotlib.pyplot as plt
import geopandas as gp
import numpy as np
import pyautogui as pag
import time
# -- coding:utf-8 --


def destination():
    plt.ion()
    villages_shp = gp.read_file(r"C:\Users\alan8\test543\project\TOWN_MOI_1090324.shp")
    villages_shp.plot(figsize=(15,10))

    plt.title('Double click your destination!')
    pos = plt.ginput(2)
    plt.pause(1)
    
    return [(pos[0][0]+pos[1][0])/2 , (pos[0][1]+pos[1][1])/2]

if __name__ == '__main__':
    print('Your destination is : ',destination())
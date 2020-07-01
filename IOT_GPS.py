import fiona
from shapely.geometry import shape, Point
import os


def search(longitude=120.999686 , latitude=24.7851415 ):  #尋找鄉鎮
    global areas, townnames
    return next((townnames[town_id]  #如果鄉鎮包含傳入的經緯度，就回傳townnames[town_id]
                 for town_id in areas  #其他就回傳NONE
                 if areas[town_id].contains(Point(longitude, latitude))),None)



def your_location(longitude=120.999686 , latitude=24.7851415):
    global areas,townnames

    dir = os.path.dirname(__file__)
    taiwan = fiona.open(os.path.join(dir, 'TOWN_MOI_1090324.shp')) #shp、dbf、shx 檔案要放在目錄下
    areas = {}
    townnames = {}

    for township in taiwan:
        town_id = township['properties']['TOWNCODE']  #鄉鎮代碼
        areas[town_id] = shape(township['geometry'])  #鄉鎮界限經緯度
        townnames[town_id] = township['properties']['TOWNNAME'] + ', ' + township['properties']['COUNTYNAME'] #search函式傳回值
    
    location = search(longitude,latitude)
    '''
    if location == None:
        print('{0:4g}\t{1:4g} is not in Taiwan'.format(longitude,latitude)) #把台灣當嗽嘎左耶喔
    else:
        print(location) #台灣NO.1
    '''
    return location #location 有可能是 None



if __name__ == '__main__':
    #此座標需要經過經緯度轉換 不可以有秒
    #https://sample.diary.tw/18/maps.htm可以幫你換算
    longitude = float(input('經度：'))
    latitude = float(input('緯度：'))
    your_location(longitude,latitude)
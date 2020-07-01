import re
import requests as req
from bs4 import BeautifulSoup as Soup
from uuid import _random_getnode as getnode
from iottalkpy.dan import NoData
import IOT_destination
import IOT_GPS 

api_url = 'https://iottalk2.tw/csm'

device_name = 'WEATHER_POSTER'

device_addr = "{:012X}".format(getnode())
print(device_addr)

# [OPTIONAL] If the device_addr is set as a fixed value, user can enable
# this option and make the DA register/deregister without rebinding on GUI
# persistent_binding = True

username = 'nctucsthegreat'

device_model = 'Dummy_Device'

idf_list = ['Dummy_Sensor']
odf_list = ['Dummy_Control']

push_interval = 1  # global interval
interval = {}

# construct a dictionary of chinese name and url
url_dict = {}
with open(r"C:\Users\alan8\test543\project\url_dictionary.txt","r") as f:
    while True:
        name = f.readline()
        url  = f.readline()
        if not name or not url: break
        name = name.replace('\n','')
        url_dict[name] = url

# Point out the destination on the map of Taiwan , output format [lng,lat]
def select_destination():
    return IOT_destination.destination()

# Change longitude and latitude to chinese name
def convert_to_name(longitude=120.999686 , latitude=24.7851415):
    return IOT_GPS.your_location(longitude,latitude)

# The destination location @weather.com
def weather_url(location):
    try : 
        return url_dict[location]
    except:
        print('Location does not exist!')

def on_register():
    print('register successfully')


def Dummy_Sensor():
    coordinate = select_destination()
    location = convert_to_name(coordinate[0],coordinate[1])
    _url = weather_url(location)
    
    r = req.get(_url)
    if r.ok:
        soup = Soup(r.text, 'html.parser')
        wind = soup.find('span', {'data-testid': 'Wind'})
        wind_deg = 180
        try:
            wind_deg = (int(re.search(
                r'transform:rotate\(([0-9]+)deg\)', wind.find('svg')['style']).group(1)) + 180) % 360
        except:
            pass
        wind_speed = float(re.search(r'([0-9]+\.?[0-9]*)', wind.text).group(1))
        visibility = float(re.search(
            r'([0-9]+\.?[0-9]*)', soup.find('span', {'data-testid': 'VisibilityValue'}).text).group(1))
        return wind_deg, wind_speed, visibility
    return ""


def Dummy_Control(data):
    pass

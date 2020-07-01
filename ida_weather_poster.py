import re
import requests as req
from bs4 import BeautifulSoup as Soup
from uuid import _random_getnode as getnode
from iottalkpy.dan import NoData

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

# The destination location @weather.com
_url = 'https://weather.com/zh-TW/weather/today/l/7ceb69e37a100e138b92e592f2bd6619cfa4626f7315d0877b5061494e83bb77'  # Hsinchu


def on_register():
    print('register successfully')


def Dummy_Sensor():
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

import time
import DAN
import threading
import sys
import re
import requests as req
from bs4 import BeautifulSoup as Soup
import json

# Select destination
url_dict = {}
with open('url_dictionary.json', 'r', encoding='utf-8') as f:
    url_dict = json.load(f)
for i, v in enumerate(url_dict.keys()):
    print(f'{str(i).zfill(2)}: {v}')
key1 = list(url_dict.keys())[int(input('Select the destination (index):'))]
for i, v in enumerate(url_dict[key1].keys()):
    print(f'{str(i).zfill(2)}: {v}')
key2 = list(url_dict[key1].keys())[
    int(input('Select the destination (index):'))]
_url = url_dict[key1][key2]

ServerURL = 'http://2.iottalk.tw:9999'  # with SSL secure connection
mac_addr = '214-fin-weatpost'
Reg_addr = mac_addr

DAN.profile['dm_name'] = 'Dummy_Device'
DAN.profile['df_list'] = ['Dummy_Sensor', 'Dummy_Control']
DAN.profile['d_name'] = '214-fin-weatposter'
DAN.device_registration_with_retry(ServerURL, Reg_addr)

# global gotInput, theInput
gotInput = False
theInput = []
allDead = False


def doRead():
    global gotInput, theInput
    while True:
        if gotInput:
            time.sleep(0.5)
            continue  # go back to while
        try:
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
                wind_speed = float(
                    re.search(r'([0-9]+\.?[0-9]*)', wind.text).group(1))
                visibility = float(re.search(
                    r'([0-9]+\.?[0-9]*)', soup.find('span', {'data-testid': 'VisibilityValue'}).text).group(1))
                theInput = [wind_deg, wind_speed, visibility]
            else:
                theInput = []
        except Exception as e:  # KeyboardInterrupt:
            print(e)
            allDead = True
            print("\n\nDeregister " +
                  DAN.profile['d_name'] + " !!!\n",  flush=True)
            DAN.deregister()
            sys.stdout = sys.__stdout__
            sys.exit()  # break  # raise   #  ?
        gotInput = True


# creat a thread to do Input data from keyboard, by tsaiwn@cs.nctu.edu.tw
threadx = threading.Thread(target=doRead)
threadx.daemon = True
threadx.start()

while True:
    try:
        # Push data to a device feature called "Dummy_Sensor"
        if gotInput:
            gotInput = False   # so that you can input again
            if(allDead):
                break
            DAN.push('Dummy_Sensor', theInput[0], theInput[1], theInput[2])

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)
    try:
        time.sleep(0.5)
    except KeyboardInterrupt:
        break
time.sleep(0.5)
try:
    DAN.deregister()
except Exception as e:
    print("===")
print("Bye ! --------------", flush=True)
sys.exit()

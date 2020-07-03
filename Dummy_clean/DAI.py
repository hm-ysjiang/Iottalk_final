import time
from . import DAN
import requests
import random
import threading
import sys

ServerURL = 'http://6.iottalk.tw:9999'  # with SSL secure connection
mac_addr = '214-dm-ptr'
Reg_addr = mac_addr

DAN.profile['dm_name'] = 'Dummy_Device'
DAN.profile['df_list'] = ['Dummy_Sensor', 'Dummy_Control']
DAN.profile['d_name'] = '214-DummyPrinter'
DAN.device_registration_with_retry(ServerURL, Reg_addr)

# global gotInput, theInput
gotInput = False
theInput = ""
allDead = False


def doRead():
    global gotInput, theInput
    while True:
        if gotInput:
            time.sleep(0.5)
            continue  # go back to while
        try:
            theInput = ""
        except Exception:  # KeyboardInterrupt:
            allDead = True
            print("\n\nDeregister " +
                  DAN.profile['d_name'] + " !!!\n",  flush=True)
            DAN.deregister()
            sys.stdout = sys.__stdout__
            print(" Thread say Bye bye ---------------", flush=True)
            sys.exit()  # break  # raise   #  ?
        gotInput = True


# creat a thread to do Input data from keyboard, by tsaiwn@cs.nctu.edu.tw
threadx = threading.Thread(target=doRead)
threadx.daemon = True
threadx.start()

while True:
    try:
        # Pull data from a device feature called "Dummy_Control"
        data = DAN.pull('Dummy_Control')
        if data != None:
            print(data)

    # Push data to a device feature called "Dummy_Sensor"
        if gotInput:
            if theInput == 'quit' or theInput == "exit":
                break  # sys.exit( )
            gotInput = False   # so that you can input again
            if(allDead):
                break
            DAN.push('Dummy_Sensor', theInput)

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

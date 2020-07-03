import time
import DAN
import requests
import random
import threading
import sys
import os

ServerURL = 'http://2.iottalk.tw:9999'
mac_addr = '214-dm-msg'
Reg_addr = mac_addr

DAN.profile['dm_name'] = 'Dummy_Device'
DAN.profile['df_list'] = ['Dummy_Sensor', 'Dummy_Control']
DAN.profile['d_name'] = '214-ServerMsg'
DAN.device_registration_with_retry(ServerURL, Reg_addr)
websock_server_path = os.path.dirname(
    os.path.realpath(__file__)) + '/../WebSock/server/'
websock_msg_file = websock_server_path + 'msg'

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

wind_lim = 21
visibility_lim = 15
prevMsg = 'fak'

while True:
    try:
        data = DAN.pull('Dummy_Control')
        if data != None:
            data = data[0]
            msg = ''
            if data[0] == 1:  # weather
                windir, speed, visi = data[1]
                if speed > wind_lim:
                    msg += 'WindSpeed too fast; '
                if visi < visibility_lim:
                    msg += 'Visibility too low; '
            elif data[0] == 2:  # accel
                ax, ay, az = data[1]
                if az < 3:
                    msg += 'Elite flying skill; '
            if msg != '' and msg != prevMsg:
                print(msg)
                os.system('echo -n "' + msg + '" > ' + websock_msg_file)
                prevMsg = msg
        # elif gotInput:
        #     if theInput == 'quit' or theInput == "exit":
        #         break  # sys.exit( )
        #     gotInput = False   # so that you can input again
        #     if(allDead):
        #         break
        #     msg = str(theInput)
        #     os.system('echo -n ' + msg + ' > ' + websock_msg_file)

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)
    try:
        time.sleep(3)
    except KeyboardInterrupt:
        break
time.sleep(0.5)
try:
    DAN.deregister()
except Exception as e:
    print("===")
print("Bye ! --------------", flush=True)
sys.exit()

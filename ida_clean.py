from uuid import _random_getnode as getnode

from iottalkpy.dan import NoData

api_url = 'https://iottalk2.tw/csm'

device_name = 'Dummy Printer'

device_addr = "{:012X}".format(getnode())
print(device_addr)

username = 'nctucsthegreat'

device_model = 'Dummy_Device'

idf_list = ['Dummy_Sensor']
odf_list = ['Dummy_Control']

push_interval = 1  # global interval
interval = {}


def on_register():
    print('register successfully')


def Dummy_Sensor():
    return ""


def Dummy_Control(data):
    print(data)

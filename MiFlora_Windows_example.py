#Based on
#https://github.com/vrachieru/xiaomi-flower-care-api/ for Xiaomi Flower Care protocol
#and 
#https://bleak.readthedocs.io/en/latest/index.html and https://github.com/hbldh/bleak
# for bleak example

import platform
import logging
import asyncio
import time

from bleak import BleakClient
from bleak import _logger as logger


_BYTE_ORDER = 'little'

_CMD_BLINK_LED = bytes([0xfd, 0xff])
_CMD_REAL_TIME_READ_INIT = bytes([0xa0, 0x1f])
_CMD_HISTORY_READ_INIT = bytes([0xa0, 0x00, 0x00])
_CMD_HISTORY_READ_SUCCESS = bytes([0xa2, 0x00, 0x00])
_CMD_HISTORY_READ_FAILED = bytes([0xa3, 0x00, 0x00])

_UUID_NAME="00002a00-0000-1000-8000-00805f9b34fb"
_UUID_FIRM_BATT="00001a02-0000-1000-8000-00805f9b34fb"
_UUID_TIME="00001a12-0000-1000-8000-00805f9b34fb"
_UUID_TEMPS_REEL_ACTIVATE="00001a00-0000-1000-8000-00805f9b34fb"
_UUID_TEMPS_REEL_DATA="00001a01-0000-1000-8000-00805f9b34fb"

_UUID_HISTO_ACTIVATE="00001a10-0000-1000-8000-00805f9b34fb"
_UUID_HISTO_DATA_READ="00001a11-0000-1000-8000-00805f9b34fb"

async def run(address, loop, debug=False):
    if debug:
        import sys

        loop.set_debug(True)
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)

    client = BleakClient(address, loop=loop)
    x= await client.connect(timeout=10.0)

    value = await client.read_gatt_char(_UUID_NAME)
    print("Name:",''.join(map(chr, value)))
    
    value = await client.read_gatt_char(_UUID_FIRM_BATT)
    print("Firmware version:",''.join(map(chr, value[2:])))
    print("Battery level:",value[0],"%")

    #calcul de la valeur moyenne avant/après pour être au plus juste
    # la comparaison epch / heure système est utile ensuite pour la lecture de l'historique
    start = time.time()
    value = await client.read_gatt_char(_UUID_TIME)
    print("Seconds since boot:",int.from_bytes(value, _BYTE_ORDER))
    wall_time = (time.time() + start) / 2
        
    epoch_offset = int.from_bytes(value, _BYTE_ORDER)
    epoch_time = wall_time - epoch_offset 

    #activation temps réel
    await client.write_gatt_char(_UUID_TEMPS_REEL_ACTIVATE,_CMD_REAL_TIME_READ_INIT,response=True)

    #lecture des données temps réel
    value = await client.read_gatt_char(_UUID_TEMPS_REEL_DATA)

    temperature = int.from_bytes(value[:2], _BYTE_ORDER) / 10.0
    light = int.from_bytes(value[3:7], _BYTE_ORDER)
    moisture = value[7]
    conductivity = int.from_bytes(value[8:10], _BYTE_ORDER)
    print("===== Real Time =====")
    print("Temperature:",temperature,"°C")
    print("Light:",light," lux")
    print("Moisture:",moisture,"%")
    print("Fertility:",conductivity,"µS/cm")

    print("===== Hystoric measures =====")
    #activation
    await client.write_gatt_char(_UUID_HISTO_ACTIVATE,_CMD_HISTORY_READ_INIT,response=True)
    #lecture du nombre d'item
    value = await client.read_gatt_char(_UUID_HISTO_DATA_READ)
    nb_histo=int.from_bytes(value[:2], _BYTE_ORDER)
    print(nb_histo,"value(s) stored")

    if nb_histo>0:
        for i in range(nb_histo):
            #calcul adresse
            addr=b'\xa1' + i.to_bytes(2, _BYTE_ORDER)
            await client.write_gatt_char(_UUID_HISTO_ACTIVATE,addr,response=True)
            value = await client.read_gatt_char(_UUID_HISTO_DATA_READ)

            #décodage
            dte=int.from_bytes(value[:4], _BYTE_ORDER)
            timestamp= time.strftime("%Y-%m-%d %H:%M:%S %z",time.localtime((epoch_time + dte)))
            temperature = int.from_bytes(value[4:6], _BYTE_ORDER) / 10.0
            lux= int.from_bytes(value[7:10], _BYTE_ORDER)
            light = round(int.from_bytes(value[7:10], _BYTE_ORDER)*0.06666)
            moisture = value[11]
            conductivity = int.from_bytes(value[12:14], _BYTE_ORDER)
            print("Date:{dte} > Temp:{temp}°C Moist {moist}% Light {light} mmol ({lux} Lux) Fert {fert} µS/cm".format(dte=timestamp,temp=temperature,moist=moisture,light=light,fert=conductivity,lux=lux))

    #effacer l'historique
    #VOLONTAIREMENT COMMENTE
    #await client.write_gatt_char(_UUID_HISTO_ACTIVATE,_CMD_HISTORY_READ_SUCCESS,response=True)

    #for fun: LED blink (once per writting)
    #for i in range(10):
    #   await client.write_gatt_char(_UUID_TEMPS_REEL_ACTIVATE,_CMD_BLINK_LED,response=True)


    #end
    x= await client.disconnect()

    
if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = (
        "C4:7C:8D:6B:04:52"
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, False))  # switch debug


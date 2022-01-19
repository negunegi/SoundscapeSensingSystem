#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
sys.path.append("../sensor_test/modubus_test")
sys.path.append("../sensor_test/ina_test")
sys.path.append("../image_test")
sys.path.append("../audio_test")
sys.path.append("../mqttServe_publish_test")

import logging
import time
from get_data_int_baiYe import main_baiYe
from get_data_int_irradiation import main_irradiation
from get_data_int_windSpeed import main_windSpeed
from get_data_float_chnt import main_hourMeter
from get_data_int_soil import main_soil
from audio_recording import upload_audio
import cv2
from get_data_int_battery import return_tuple
from get_the_pic import upload_pic,camera_pic_capture
from publish_single import mqtt_publish
import json

def restart_program():
    '''
    restart program
    '''
    python = sys.executable
    os.execl(python, python, * sys.argv)

#time define
logging.info('test start')
time_start = time.time()
struct_Time = time.localtime()
Time = time.strftime('%Y%m%d%H%M%S',struct_Time)
Time_for_file = time.strftime('%Y%m%d',struct_Time)
Time_for_json = time.strftime('%Y-%m-%d %H:%M:%S',struct_Time)

logging.info('sound recording')
sound_name = upload_audio(Time,Time_for_file)

logging.info('pic capturing')
camera_index = 0
_,frame,camera_index = camera_pic_capture(camera_index)
cv2.imwrite('./raw/imgv_iue002_{}.jpg'.format(Time),frame)
pic_name = upload_pic(Time,Time_for_file)


logging.info('capture data')

error_num = 0
while True:
    if error_num == 5:
        baiye_flag = False
        air_h,air_t,_,_,_,air_p,illumination_high,illumination_low = -9999,-9999,-9999,-9999,-9999,-9999,-9999,-9999
        break
    try:
        air_h,air_t,_,_,_,air_p,illumination_high,illumination_low = main_baiYe()
        break
    
    except Exception as e:
        error_num+=1
        print(e)
        continue

error_num = 0
while True:
    if error_num ==5:
        irr_flag = False
        irradiation=-9999
        break
    try:
        irradiation, = main_irradiation()
        break
    except Exception as e:
        error_num+=1
        print(e)
        continue

error_num = 0
while True:
    if error_num ==5:
        WS_flag = False
        win_speed=-9999
        break
    try:
        win_speed, = main_windSpeed()	
        break
    except Exception as e:
        error_num+=1
        print(e)
        continue

error_num = 0
while True:
    if error_num ==5:
        chnt_flag = False
        ac_v,ac_c=-9999,-9999
        break
    try:
        ac_v,ac_c,ac_p = main_hourMeter()
        break
    except Exception as e:
        error_num+=1
        print(e)
        continue
error_num = 0
while True:
    if error_num ==5:
        S_flag = False
        soil_h,soil_t=-9999,-9999
        break
    try:
        soil_h,soil_t = main_soil()
        # soil_h,soil_t = -9999,-9999

        break
    except Exception as e:
        error_num+=1
        print(e)
        continue
error_num = 0
while True:
    if error_num ==5:
        P_flag = False
        bat_v,lod_v,lod_c=-9999,-9999,-9999
        
        break
    try:
        bat_v,lod_v,lod_c = return_tuple()
        break
    except Exception as e:
        error_num+=1
        print(e)
        continue        

# time.sleep(1)
json_dict = {
"sn":"iue001",
"time":Time_for_json,
"value":{
"ac_v":round(float(ac_v),2),
"ac_c":round(float(ac_c),2),
"ac_p":round(float(ac_p),2),
"air_h":round(float(air_h)/10,2),
"air_t":round(float(air_t)/10,2),
"air_p":round(float(air_p)/10,2),
"illumination":int('{}{}'.format(illumination_high,illumination_low)),
"irradiation":round(float(irradiation),2),
"win_speed":round(float(win_speed),2),
"soil_h":round(float(soil_h)/10,2),
"soil_t":round(float(soil_t)/10,2),
"audio":sound_name,
"imgv":pic_name,
"bat_v":round(float(bat_v),2),
"lod_v":round(float(lod_v),2),
"lod_c":round(float(lod_c),2)}
}
print("封装数据:",json_dict)
json_send = json.dumps(json_dict)
mqtt_publish('soundscape',json_send)



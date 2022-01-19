#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import threading
root_file = '/home/pi/code_test'
sys.path.append("{}/sensor_test/modubus_test".format(root_file))
sys.path.append("{}/sensor_test/ina_test".format(root_file))
sys.path.append("{}/image_test".format(root_file))
sys.path.append("{}/audio_test".format(root_file))
sys.path.append("{}/mqttServe_publish_test".format(root_file))

import logging
import time
from get_data_int_baiYe import main_baiYe
from get_data_int_irradiation import main_irradiation
from get_data_int_windSpeed import main_windSpeed
from get_data_float_chnt import main_hourMeter
from get_data_int_soil import main_soil
from img_add_text import add_time_text    
import cv2
from get_data_int_battery import return_tuple
from get_the_pic import upload_pic,camera_pic_capture
from publish_single import mqtt_publish
import json
import traceback
from audio_recording import audio_recording_func
from audio_recording import audio_upload
import random
import configparser
#draw 
import spidev as SPI

cf = configparser.ConfigParser()
cf.read('/home/pi/site_info.ini')
site_no = cf.get('site_info','site_no')#loading cofig file

#define thread
def dec2hex2dec(high_position,low_position):##format the high and low position value.
    hex_high = format(int(high_position),'x')
    hex_low = format(int(low_position),'x')
    return int('{}{:0>4}'.format(hex_high,hex_low),16)

class sensorThread(threading.Thread):
    def __init__(self,func,args=()):
        super(sensorThread,self).__init__()
        self.func = func
        self.args = args
    def run(self):
        self.result = self.func(*self.args)
    def get_result(self):
        try:
            return self.result # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception as e:
            traceback.print_exc(file=open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+'))
            with open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+') as f:
                f.write('于{}发生{}错误'.format(time.strftime('%Y_%m_%d_%H_%M_%S'),e))
                f.write('=========================================================\n')
            return None

def audio_recording_showing_func(Time):#execute the audio recording and return the audio file name.
    
    NAME = audio_recording_func(Time)

    return NAME

def pic_capturing_func(Time,Time_for_json):#execute the photo capturinf and return the picture file name.

        camera_index = 0
        _,frame,camera_index = camera_pic_capture(camera_index)
        frame_has_text =  add_time_text(Time_for_json,site_no,frame)
        pic_name = 'imgv_{}_{}.jpg'.format(site_no,Time)
        cv2.imwrite('./raw/{}'.format(pic_name),frame_has_text)
        return pic_name

def baiYe_reading_func(*add_lists):#reading the sensor data.baiYe is a sensor which can capture air_humidity,air_temporary,air_pressure and illumination. if it failed 10 times,-9999 will be returned.
    error_num = 0
    while True:
        if error_num == 10:
            air_h,air_t,_,_,_,air_p,illumination_high,illumination_low = -9999,-9999,-9999,-9999,-9999,-9999,-9999,-9999
            illumination = -9999
            add_lists[0].append(air_h)
            add_lists[1].append(air_t)
            add_lists[2].append(air_p)
            add_lists[3].append(illumination)
            break
        try:
            air_h,air_t,_,_,_,air_p,illumination_high_raw,illumination_low_raw = main_baiYe()
            illumination = dec2hex2dec(illumination_high_raw,illumination_low_raw)
            add_lists[0].append(air_h)
            add_lists[1].append(air_t)
            add_lists[2].append(air_p)
            add_lists[3].append(illumination)
            break
        
        except Exception as e:
            error_num+=1
            print(e)
            continue

def irradiation_reading_func(add_list):#reading the irradiation sensor data.
    error_num = 0
    while True:
        if error_num ==10:
            irradiation=-9999
            add_list.append(irradiation)
            break

        try:
            irradiation, = main_irradiation()    
            add_list.append(irradiation)
            break
        except Exception as e:
            error_num+=1
            print(e)
            continue

def windSpeed_reading_func(add_list):#reading the wind speed sensor data.
    error_num = 0
    while True:
        if error_num ==10:
            win_speed=-9999
            add_list.append(win_speed)
            break

        try:
            win_speed, = main_windSpeed()
            add_list.append(win_speed)
            break
        except Exception as e:
            error_num+=1
            print(e)
            continue

def hourMeter_reading_func():#reading the power supply sensor data
    error_num = 0

    while True:
        if error_num ==10:
            ac_v,ac_c,ac_p=-9999,-9999,-9999
            return ac_v,ac_c,ac_p
        try:
            ac_v,ac_c,ac_p = main_hourMeter()
            return ac_v,ac_c,ac_p

        except Exception as e:
            error_num+=1
            print(e)
            continue

def soil_reading_func(*add_lists):#reading the soil temperature and humidity sensor data
    error_num = 0
    while True:
        if error_num ==10:
            soil_h,soil_t=-9999,-9999
            add_lists[0].append(soil_h)
            add_lists[1].append(soil_t)
            break
        try:
            soil_h,soil_t = main_soil()
            add_lists[0].append(soil_h)
            add_lists[1].append(soil_t)
            break

        except Exception as e:
            error_num+=1
            print(e)
            continue

def bat_reading_func():#reading the battery situation data.
    error_num = 0
    while True:
        if error_num ==10:
            bat_v,lod_v,lod_c=-9999,-9999,-9999
            return bat_v,lod_v,lod_c
        try:
            bat_v,lod_v,lod_c = return_tuple()
            return bat_v,lod_v,lod_c
        except Exception as e:
            error_num+=1
            print(e)
            continue


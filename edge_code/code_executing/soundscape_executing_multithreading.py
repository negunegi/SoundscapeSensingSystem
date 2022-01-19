#!/usr/bin/python
# -*- coding: UTF-8 -*-



import os
import sys 
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


root_file = '/home/pi/code_test'
sys.path.append("{}/mqttServe_publish_test".format(root_file))
sys.path.append("{}/audio_test".format(root_file))
sys.path.append("{}/sqllite_test".format(root_file))
sys.path.append("{}/control_test".format(root_file))


from soundscape_thread_pools_realData import *

import logging
import time
import cv2
from publish_single import mqtt_publish
import json
import traceback
from sqllite_executing import sqllite_main
from check_and_upload_process import check_and_upload_func
from fan_tem_control import fan_control,judge
from threading import Thread
import RPi.GPIO as GPIO
import socket
import configparser
from sqllite_check_and_upload import sqllite_check_and_upload
#config
cf = configparser.ConfigParser()
cf.read('/home/pi/site_info.ini')
site_no = cf.get('site_info','site_no')


#fan GPIO define
FAN_GPIO = 4 #raspi pin for fan
GPIO.setmode(GPIO.BCM)
#define thread
#config

def restart_program():#restart the .py file.
    '''
    restart program
    '''
    python = sys.executable
    os.execl(python, python, * sys.argv)


logging.info('capture data')
#upload_thread_start
upload_thread = Thread(target=check_and_upload_func,args=('/home/pi/code_executing/raw',))#creating thread for upload file.
upload_thread.start()
#fan_thread_start
fan_thread = Thread(target=fan_control)#creating thread for fan control function.
fan_thread.start()
#sqllite_upload
sqllite_upload_thread = Thread(target=sqllite_check_and_upload,args=('sound_env.db','sound_env_b.db'))#creating sqllite upload thread using two database to avoid upload function and insert function use the database at the same time.
sqllite_upload_thread.start()
def main_for_collection():#main function
    try:
        time_start = time.time()

        struct_Time = time.localtime()
        Time = time.strftime('%Y%m%d%H%M%S',struct_Time)
        Time_for_json = time.strftime('%Y-%m-%d %H:%M:%S',struct_Time)
        scheduler = BackgroundScheduler()#creating the total scheduler

        air_h_list = []#air_humidity
        air_t_list = []#air_temporary
        air_p_list = []#air_pressure 
        illumination_list = []#illumination
        irradiation_list = []#irradiation
        soil_h_list = []#soil_humidity
        soil_t_list = []#soil_temporary
        windSpeed_list = []#wind speed

        ele_list = [air_h_list,air_t_list,air_p_list,illumination_list,irradiation_list,soil_h_list,soil_t_list,windSpeed_list]#total list

        baiYe_reading_func(air_h_list,air_t_list,air_p_list,illumination_list)#get air_humidity,air_temporary,air_pressure and illumination at first time
        irradiation_reading_func(irradiation_list)#get irradiation at first time
        windSpeed_reading_func(windSpeed_list)#get windspeed at first time
        soil_reading_func(soil_h_list,soil_t_list)#get soil humidity and soil temporary at first time.

        scheduler.add_job(baiYe_reading_func, args=[air_h_list,air_t_list,air_p_list,illumination_list],
            trigger="cron", second='0/10')#set a scheduler to get air_humidity,air_temporary,air_pressure and illumination every 10 secs.
        scheduler.add_job(irradiation_reading_func, args=[irradiation_list],
            trigger="cron", second='0/10')#set a scheduler to get irradiation every 10 secs.
        scheduler.add_job(windSpeed_reading_func, args=[windSpeed_list],
            trigger="cron", second='0/2')#set a scheduler to get wind speed every 2 secs.
        scheduler.add_job(soil_reading_func, args=[soil_h_list,soil_t_list],
            trigger="cron", second='0/10')#set a scheduler to get soil_humidity and soil_temporary every 2 secs.

        scheduler.start()
        print('done')

        while True:
            if all([len(i)>=q for i,q in zip(ele_list,(5,5,5,5,5,5,5,29))]):#judge whether the system collect enough data in 1 minute.(windspeed should have 30 values,others 6.)

                # air_h_list = air_h_list.remove(max(air_h_list)).remove(min(air_h_list))
                air_t_list.sort()
                air_h_list.sort()
                air_p_list.sort()
                illumination_list.sort()
                irradiation_list.sort()
                soil_t_list.sort()
                soil_h_list.sort()
                windSpeed_list.sort()#values are arranged from small to large.

                air_t_list = air_t_list[1:-1]
                air_h_list = air_h_list[1:-1]
                air_p_list = air_p_list[1:-1]
                illumination_list = illumination_list[1:-1]
                irradiation_list = irradiation_list[1:-1]
                soil_t_list = soil_t_list[1:-1]
                soil_h_list = soil_h_list[1:-1]
                windSpeed_list = windSpeed_list[1:-1]#drop the largest and least value

                air_h = sum(air_h_list)/len(air_h_list)
                air_t = sum(air_t_list)/len(air_t_list)
                air_p = sum(air_p_list)/len(air_p_list)
                illumination = sum(illumination_list)/len(illumination_list)
                irradiation = sum(irradiation_list)/len(irradiation_list)
                soil_t = sum(soil_t_list)/len(soil_t_list)
                soil_h = sum(soil_h_list)/len(soil_h_list)
                windSpeed = sum(windSpeed_list)/len(windSpeed_list)#count the average of data
                break
            else:
                time.sleep(1)
                continue#keep watch whether the system has collected data.

        scheduler.shutdown(wait=False)#clouse the scheduler

        fan_mode,cpu_temp = judge(FAN_GPIO)#get the fan mode and cpu temporary

        pic_name = pic_capturing_func(Time,Time_for_json)#get the picture name

        ac_v,ac_c,ac_p= hourMeter_reading_func()#get the supply of electricity mode

        bat_v,lod_v,lod_c = bat_reading_func()#get the battery mode.

        time.sleep(0.1)

        sound_name = audio_recording_showing_func(Time)# get the audio file name

        json_dict = {
        "sn":site_no,
        "time":Time_for_json,
        "value":{
        "ac_v":round(float(ac_v),1),
        "ac_c":round(float(ac_c),2),
        "ac_p":round(float(ac_p),2),
        "air_h":round(float(air_h)/10,1),
        "air_t":round(float(air_t)/10,1),
        "air_p":round(float(air_p)/10,1),
        "illumination":int(illumination),
        "irradiation":round(float(irradiation),1),
        "win_speed":round(float(windSpeed)/10,1),
        "soil_h":round(float(soil_h)/10,1),
        "soil_t":round(float(soil_t)/10,1),
        "audio":sound_name,
        "imgv":pic_name,
        "bat_v":round(float(bat_v),1),
        "lod_v":round(float(lod_v),1),
        "lod_c":round(float(lod_c),1),
        "cpu":cpu_temp,
        "fan":fan_mode}
        }
        print("Encapsulating data:",json_dict)
        try:
            json_send = json.dumps(json_dict)
            mqtt_publish('soundscape',json_send)#publish the encaosulated data to mqtt server


        except Exception as e:#when network is obstructed,data will be stored in sqllite database temporarily.
            try:
                sqllite_main('sound_env.db',json_dict)
            except Exception as e_2:#when the database is used by upload func , system will store data in backup database.
                sqllite_main('sound_env_b.db',json_dict)
            traceback.print_exc(file=open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+'))
            print(e)
            with open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+') as f:
                f.write('in {},{} error happened'.format(time.strftime('%Y_%m_%d_%H_%M_%S'),e))
                f.write('data did not publish and was stored in sqllite database.this circle started in {}'.format(time.strftime('%Y-%m-%d %H:%M:%S',struct_Time)))
                f.write('=========================================================\n')
        length = len(threading.enumerate())
        print('thread number ：%d' % length)
            
    except socket.timeout as e:
        time.sleep(5)
    except Exception as e:
        traceback.print_exc(file=open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+'))
        with open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+') as f:
            f.write('in {},{} error happened'.format(time.strftime('%Y_%m_%d_%H_%M_%S'),e))
            f.write('program restart.\n')
            f.write('=========================================================\n')

scheduler_for_collection =BlockingScheduler()
scheduler_for_collection.add_job(main_for_collection,
            trigger="cron", minute='0/2',second='0')#every two minute execute the main function
scheduler_for_collection.start()

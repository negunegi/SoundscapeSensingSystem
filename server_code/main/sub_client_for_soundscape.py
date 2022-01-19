## -*- coding: utf-8 -*-
# import context  # Ensures paho is in PYTHONPATH
import os
import sys
import paho.mqtt.subscribe as subscribe
import json
import time
root_file = os.path.dirname(os.path.dirname( __file__))
sys.path.append(root_file)
from push_to_sql.connection import *
import paho.mqtt.client as mqtt
from sqlite_coding.sqllite_executing import  sqllite_main
import traceback

def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))
    mqttc.subscribe('soundscape', 0)

def on_message(mqttc, obj, msg):
    try:
        data = json.loads(msg.payload)
    except Exception as e:
        print('%s error happened'%(e),'decoding failed.')
        return None
    
    print(str(msg.payload,encoding='utf-8'))
    try:
        # time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['ts']/1000))
        time_stamp = data['time']
        # database_name = data['sn']+'_'+data['id']   
        database_name = data['sn']
    except Exception as e:
        print('%s error happened'%(e),'skipping this data')
        return None
        
    print(database_name)
    print(time_stamp)
 
    cursor = connect.cursor()
    # print(connect)
    # print(str(msg.payload,encoding='utf-8'))
    #print('insert into %s(data_time,value) values(\'%s\',\'%s\')'%(database_name,time_stamp,str(msg.payload,encoding='utf-8')))
    try:

        cursor.execute('insert into %s(data_time,value) values(\'%s\',\'%s\')'%(database_name,time_stamp,str(msg.payload,encoding='utf-8')))
        print('inseted successfully')
    except Exception as e:
        try:
         sqllite_main(database_name,'sound_env.db',data)

        except Exception as e_2:
           sqllite_main(database_name,'sound_env_b.db',data)
        traceback.print_exc(file=open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+'))
        print(e)
        with open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+') as f:
         f.write('in {} , {} error happened'.format(time.strftime('%Y_%m_%d_%H_%M_%S'),e))
         f.write('data did not write and was stored in database.')
         f.write('=========================================================\n')
        


    connect.commit()  #提交


def on_publish(mqttc, obj, mid):
    # print("mid: "+str(mid))
    pass

def on_subscribe(mqttc, obj, mid, granted_qos):
    # print("Subscribed: "+str(mid)+" "+str(granted_qos))
    pass

def on_log(mqttc, obj, level, string):
   if level == 8:
     with open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+') as f:
         print(string)
         f.write('in {} , {} error happened'.format(time.strftime('%Y_%m_%d_%H_%M_%S'),e))
         f.write('=========================================================\n')


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.

connect = conn()
mqttc = mqtt.Client('Your mqtt client name',clean_session=True)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
            # Uncomment to enable debug messages
mqttc.username_pw_set('Your mqtt user',password='Your mqtt password')
mqttc.on_log = on_log
mqttc.reconnect_delay_set(min_delay=1, max_delay=5)
mqttc.connect('Your mqtt server host.', 'Your mqtt server port.', 5)


mqttc.loop_forever()

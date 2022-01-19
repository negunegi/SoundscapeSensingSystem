import paho.mqtt.publish as publish
import json
import time

def mqtt_publish(topics,json_dict):#publish a single message to mqtt server.
    publish.single(topic=topics,payload=json_dict,qos=0,hostname='Your mqtt host name'\
    ,port=1883,auth={'username':'Your mqtt server username','password':'Your mqtt server password'},keepalive=5)

if __name__ == "__main__":
    topics = 'soundscape_offline'
    dicts = {'sn': 'iue001', 'time': '2021-01-28 22:29:16', 'value': {'ac_v': 217.1, 'ac_c': 0.07, 'ac_p': 1.5, 'air_h': 78.4, 'air_t': 13.7, 'air_p': 102.5, 'illumination': 0, 'irradiation': 0.0, 'win_speed': 0.0, 'soil_h': -1.0, 'soil_t': -1.0, 'audio': 'audio_iue001_20210128222916.wav', 'imgv': 'imgv_iue001_20210128222916.jpg', 'bat_v': 12.4, 'lod_v': 12.36, 'lod_c': 0.44}}
    payloads = json.dumps(dicts)
    count = 0
    try:
        while True:
            publish.single(topic=topics,payload=payloads,qos=0,hostname='Your mqtt host name'\
    ,port=1883,auth={'username':'Your mqtt server username','password':'Your mqtt server password'},keepalive=5)
            print('data has been published to mqtt server.')
            time.sleep(3)
            count+=1
    except KeyboardInterrupt:
        print(count)

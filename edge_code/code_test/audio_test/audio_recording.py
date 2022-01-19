import os 
import time
from upload import ftp_upload
import configparser

cf = configparser.ConfigParser()
cf.read('/home/pi/site_info.ini')
site_no = cf.get('site_info','site_no')

TIME = 5
RATE = 44100
CHANNELS = 1


def audio_recording_func(Time):#record audio function
    NAME = time.strftime('audio_{}_{}.wav'.format(site_no,Time))
    os.system("arecord --device=plughw:1,0 --format S24_3LE --rate {} -c {} -d {} \
    ./raw/{}".format(RATE,CHANNELS,TIME,NAME))
    
    return NAME

def audio_upload(NAME,Time_for_file):#audio upload function for test
     ftp_upload('./raw/{}'.format(NAME),'{}/{}/{}'.format(site_no,Time_for_file,NAME))
     os.system('sudo rm ./raw/{}'.format(NAME))

def audio_for_test():#test function for audio recording.
    Time = time.strftime('%Y%m%d%H%M%S')
    NAME = time.strftime('audio_{}_{}.wav'.format(site_no,Time))
    os.system("arecord --device=plughw:1,0 --format S24_3LE --rate {} -c {} -d {} \
    ./{}".format(RATE,CHANNELS,TIME,NAME))
    # ftp_upload('./RAW/{}'.format(NAME),'cateen_test/{}'.format(NAME))
    # os.system('sudo rm ./RAW/{}'.format(NAME))
    return NAME,size
    
if __name__ == "__main__":
    audio_for_test()
    
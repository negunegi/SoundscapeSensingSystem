import cv2
import sys
from PIL import Image,ImageDraw,ImageFont
import os 
import time
from upload import ftp_upload
import configparser

cf = configparser.ConfigParser()
cf.read('/home/pi/site_info.ini')
site_no = cf.get('site_info','site_no')
# dev_num = 0

def camera_pic_capture(camera_index):#photo function
    ret = False
    error_num = 0
    while not ret:
        cap = cv2.VideoCapture(camera_index)#get the picture
        cap.set(3,1920)#set picture width
        cap.set(4,1080)#set picture height
        ret, frame = cap.read()
        x, y = frame.shape[0:2]
        frame =  cv2.resize(frame, (int(y / 2), int(x / 2)))#resize the picture
        error_num+=1
        camera_index+=1
        if error_num == 10:
            break
    return ret,frame,camera_index

#upload pic test code
def upload_pic(Time,Time_for_file):

    NAME = time.strftime('imgv_{}_{}.jpg'.format(site_no,Time))
    ftp_upload('./raw/{}'.format(NAME),'{}/{}/{}'.format(site_no,Time_for_file,NAME))
    os.system('sudo rm ./raw/{}'.format(NAME))
    return NAME

if __name__ == "__main__":
    Time = time.strftime('%Y%m%d%H%M%S')
    pic_ret,pic_frame,_ = camera_pic_capture(0)
    
    cv2.imwrite('imgv_iue003_{}.jpg'.format(Time),pic_frame)
    print(pic_ret)


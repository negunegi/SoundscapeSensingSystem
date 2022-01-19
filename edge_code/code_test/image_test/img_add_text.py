import cv2
import time
from get_the_pic import camera_pic_capture


Time_now = time.localtime()
Time_for_json = time.strftime('%Y-%m-%d %H:%M:%S',Time_now)
# img = cv2.imread('20210130215407.jpg')
# img2 = img.copy()  # 备份操作

def add_time_text(Time,tag,frame):#add character to picture
    font = cv2.FONT_HERSHEY_PLAIN  # define the font
    imgzi_frame = cv2.putText(frame, Time, (10, 35), font, 1.2, (0, 0, 192), 2)#put text
    imgzi_frame = cv2.putText(imgzi_frame, tag, (10, 15), font, 1.2, (0, 0, 192), 2)#put text
    return imgzi_frame

if __name__ == "__main__":
    pic_ret,pic_frame,_ = camera_pic_capture(0)
    struct_Time = time.localtime()
    Time_for_json = time.strftime('%Y-%m-%d %H:%M:%S',struct_Time)
    pic_zi_frame = add_time_text(Time_for_json,'iue002',pic_frame)
    cv2.imwrite('./img_zizi.jpg',pic_zi_frame)
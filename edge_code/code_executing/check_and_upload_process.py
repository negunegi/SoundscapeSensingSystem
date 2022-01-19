import os
import time
import traceback
from upload import ftp_upload
import configparser
import sys

cf = configparser.ConfigParser()
cf.read('/home/pi/site_info.ini')#the path to put your site information config
site_no = cf.get('site_info','site_no')
root_file =  '/home/pi/code_test'# the code_test file path
sys.path.append("{}/sqllite_test".format(root_file)) 
from sqllite_check_and_upload import sqllite_check_and_upload_main

def check_and_upload_func(path): # this function will check the path file which ends with 'jpg' and 'wav' and upload it to remote ftp server if network is unobstructed.
   #path: the temporay file store path in edge computer.
    while True:
        time_round = int(time.time())
        try:
            for root,_,files in os.walk(path):
                if len(files) <2:# if path has less than 2 file, it will be standy for 25 seconds.
                    time.sleep(25)
                else:
                    for file_name in files:# if the audio file is created within 10 seconds from now,the system will skip it to avoid uploading incomplete audio file(the sound is still recording when uploading.)

                        if file_name.endswith('.wav'):
                            struct_time = time.strptime(file_name[13:27],'%Y%m%d%H%M%S')
                            file_time = int(time.mktime(struct_time))
                            if abs(time_round - file_time) > 10:
                                Time_for_file = time.strftime('%Y%m%d',struct_time)
                                ftp_upload(os.path.join(root,file_name),'{}/{}/{}'.format(site_no,Time_for_file,file_name))
                                print(abs(time_round - file_time))
                                os.system('sudo rm {}'.format(os.path.join(root,file_name)))

                            else:
                                pass
                        
                        elif file_name.endswith('.jpg'):# upload picture file

                            struct_time = time.strptime(file_name[12:26],'%Y%m%d%H%M%S')
                            Time_for_file = time.strftime('%Y%m%d',struct_time)
                            ftp_upload(os.path.join(root,file_name),'{}/{}/{}'.format(site_no,Time_for_file,file_name))
                            os.system('sudo rm {}'.format(os.path.join(root,file_name)))
                    

                        else :#if file doesn't end with 'jpg' or 'wav',it will be removed.
                            os.system('sudo rm {}'.format(os.path.join(root,file_name)))



                            
        except Exception as e:#log will be written if some bugs happened.
            traceback.print_exc(file=open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+'))
            with open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a') as f:
                f.write('in {},{} error happened'.format(time.strftime('%Y_%m_%d_%H_%M_%S'),e))
                f.write('=========================================================\n')
            time.sleep(120)





if __name__ == "__main__":
    check_and_upload_func('/home/pi/code_executing/raw')

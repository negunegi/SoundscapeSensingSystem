# -*- coding: UTF-8 -*-

from ftplib import FTP_TLS
import os
import os.path

def ftp_upload(filename, save_filename):
    ftp = FTP_TLS()
    ftp.set_debuglevel(0)                   
    ftp.connect(host='Your ftp host name', port='Your ftp port', timeout=60)  
    ftp.login(user='Your ftp user', passwd='Your ftp password')           
    print('ftp successfully connected.')
    remote_dir = save_filename.split("/")
    newfilename = remote_dir.pop()

    if remote_dir :
        for dir_name in remote_dir :
            if dir_name == '.' or dir_name == '' :
                continue
            else :
                #尝试创建目录
                try:
                    ftp.mkd(dir_name)
                    ftp.cwd(dir_name)
                except:
                    ftp.cwd(dir_name)
    target_path = '/'.join(remote_dir)
    print ('Saving file name:', newfilename)
    print ('Upload directory:', target_path)
    print ('current directory:', ftp.pwd())
    print ('the uploading file name: %s' % os.path.basename(filename))
    bufsize = 1024                       
    file_handler = open(filename, 'rb')  
    # error_num = 0
 
    ftp.storbinary('STOR %s' % newfilename, file_handler, bufsize)
        
    ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit()
    print ("local file ", filename, " successfully upload to ", save_filename)

        #举个栗子
if __name__ == "__main__":
        
    ftp_upload(r'./test_speed.jpg', 'upload_test/test_speed.jpg')

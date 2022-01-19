import sqlite3
import json
import paho.mqtt.publish as publish
import json
import time
import traceback
topics = 'soundscape'
def sqllite_check_and_upload_main(dbname):#check the sqllite database and upload the data in it.
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        cursor.execute(("SELECT *  from sound_env"))
        data = cursor.fetchall()
        if len(data) > 0:
            for row in data:
                try:
                    publish.single(topic=topics,payload=row[1],hostname='Your mqtt server hostname'\
                    ,port=1883,auth={'username':'Your user name','password':'Your pass word'},keepalive=5)
                    print('data was published to mqtt server successfully.')
                    
                    time.sleep(1)
                except Exception as e:
                    traceback.print_exc(file=open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+'))
                    with open('./log/{}.txt'.format(time.strftime('%Y%m%d')),'a+') as f:
                        f.write('in {},{} error happened'.format(time.strftime('%Y_%m_%d_%H_%M_%S'),e))
                        f.write('=========================================================\n')
                    conn.commit()
                    return

                cursor.execute("DELETE FROM sound_env WHERE time_stamp=?",(row[0],))
        conn.commit()
def sqllite_check_and_upload(dbname1,dbname2):#main function for checking sqllite database and its backup and uploading the data in them.
        while True:
            sqllite_check_and_upload_main(dbname1)
            sqllite_check_and_upload_main(dbname2)
            time.sleep(600)
if __name__ == "__main__":
    sqllite_check_and_upload('sound_env.db','sound_env_b.db')


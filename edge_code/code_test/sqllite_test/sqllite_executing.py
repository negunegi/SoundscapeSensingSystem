import sqlite3
import json
def sqllite_main(dbname,data):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    try:
        cursor.execute('''CREATE TABLE sound_env
            (time_stamp        TEXT    NOT NULL,
            value            TEXT );''')
    except sqlite3.OperationalError as e:
        pass

    time_stamp = data['time']
    json_data = json.dumps(data)
    cursor.execute('insert into sound_env(time_stamp,value) values(\'%s\',\'%s\')'%(time_stamp,json_data))
    conn.commit()


if __name__ == "__main__":
    dicts = {'sn': 'iue002', 'time': '2021-01-26 22:29:16', 'value': {'ac_v': 217.1, 'ac_c': 0.07, 'ac_p': 1.5, 'air_h': 78.4, 'air_t': 13.7, 'air_p': 102.5, 'illumination': 0, 'irradiation': 0.0, 'win_speed': 0.0, 'soil_h': -1.0, 'soil_t': -1.0, 'audio': 'audio_iue001_20210128222916.wav', 'imgv': 'imgv_iue001_20210128222916.jpg', 'bat_v': 12.4, 'lod_v': 12.36, 'lod_c': 0.44}}
    dicts_1 = {'sn': 'iue002', 'time': '2021-01-27 22:29:16', 'value': {'ac_v': 217.1, 'ac_c': 0.07, 'ac_p': 1.5, 'air_h': 78.4, 'air_t': 13.7, 'air_p': 102.5, 'illumination': 0, 'irradiation': 0.0, 'win_speed': 0.0, 'soil_h': -1.0, 'soil_t': -1.0, 'audio': 'audio_iue001_20210128222916.wav', 'imgv': 'imgv_iue001_20210128222916.jpg', 'bat_v': 12.4, 'lod_v': 12.36, 'lod_c': 0.44}}
    sqllite_main('test.db',dicts)
    sqllite_main('test.db',dicts_1)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    result = cursor.execute(("SELECT *  from sound_env"))
    for row in result:
        print(row)
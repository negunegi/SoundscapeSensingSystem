# SoundscapeSensingSystem

This repo contains code for paper: An Integrated and Smart Soundscape Sensing System for Urban Ecosystem Research.

## hardware requirement

this system need at least 1 edge computer(default Raspberry Pi) with a variety of sensors(using modbus protocol) and a server computer installing mqtt client and sql(default sqlserver).

## environments

the code has two parts: edge code for sensor data capturing and transmitting  and server code for data receiving and inserting into sql database.

The codebase is developed with Python 3.7.

the default server system is windows server R2 standard and sql database is sqlserver Install requirements as follows:

```python
pip install -r requirement_for_server.txt#install it in server
```

the default edge computer system is Raspberry Pi 4. install requirement as follows:

```python
pip install -r requirement_for_edge.txt # install it in edge computer

#cv2 installing

sudo apt-get -y update
sudo apt-get install python3-pip -y
sudo pip install opencv-python

sudo apt-get install libwebp-dev -y
sudo apt-get install libtiff-dev -y
sudo apt-get install libopenjp2-dev -y
sudo apt-get install libopenjp2-7 -y
sudo apt-get install libilmbase23 -y
sudo apt-get install libopenexr-dev -y
sudo apt-get install libavcodec-dev -y
sudo apt-get install libavformat-dev -y
sudo apt-get install libswscale-dev -y
sudo apt-get install libgtk-3-dev -y
sudo apt-get install libhdf5-dev -y
sudo apt-get install liblapack-dev -y
sudo apt-get install libatlas-base-dev -y

#fan lib installing
sudo apt-get -y install python3-rpi.gpio

#
sudo apt-get install screen -y
sudo apt-get  install sqlite sqlite3

#Raspberry config
sudo raspi-config -> Interface options -> 1-wire -> no
sudo raspi-config -> Interface options -> serial port -> yes
sudo raspi-config -> Interface options -> SPI -> yes
```

## init setting

### site information 

type your site information in ./site_info.ini,which may affect the file name.

### server's host,port,user and password

type your sql and mqtt server host,port,user and password in file. as follows:

```
.\edge_code\code_executing\sqllite_check_and_upload.py
.\edge_code\code_executing\upload.py
.\edge_code\code_test\mqttServe_publish_test\publish_single.py
.\server_code\main\sub_client_for_soundscape.py
.\SoundscapeSensingSystem\server_code\push_to_sql\connection.py
```

### modbus settings

set your modbus sensors config in  .\edge_code\code_test\sensor_test\modubus_test 

## getting started

```
cd .\edge_code\code_executing
python soundscape_executing_multithreading.py
```


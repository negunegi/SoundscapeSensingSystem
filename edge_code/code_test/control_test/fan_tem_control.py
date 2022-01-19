
#coding:utf8
import time
import RPi.GPIO as GPIO

FAN_GPIO = 4



FAN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN,GPIO.OUT,initial=GPIO.LOW)
    
#test code    
def FAN_on(FAN_name):
    GPIO.output(FAN_name,GPIO.HIGH)
def FAN_off(FAN_name):
    GPIO.output(FAN_name,GPIO.LOW)
def judge(FAN_GPIO):
    tmpFile = open( '/sys/class/thermal/thermal_zone0/temp' )
    cpu_temp_raw = tmpFile.read()
    cpu_temp = round(float(cpu_temp_raw)/1000, 1)
    if GPIO.input(FAN_GPIO):
        print('Input was HIGH')
        return 'true',cpu_temp
    else:
        print('Input was LOW')
        return 'false',cpu_temp
########
def fan_control():
    while True:


        tmpFile = open( '/sys/class/thermal/thermal_zone0/temp' )#get the cpu temperature
        cpu_temp_raw = tmpFile.read()
        tmpFile.close()
        cpu_temp = round(float(cpu_temp_raw)/1000, 1)
        # print (cpu_temp)
    
        #if the cup temperature is larger than 50°C the fun will be activate.
        if cpu_temp > 50 :
            # init(FAN_GPIO)
            GPIO.output(FAN_GPIO,GPIO.HIGH)
        ##if the cup temperature is less than 50°C the fun will be deactivate.
        elif cpu_temp < 45 :
            GPIO.output(FAN_GPIO,GPIO.LOW)

        time.sleep(3)


        
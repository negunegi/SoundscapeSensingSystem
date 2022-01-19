import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import struct

def dec2hex2dec(high_position,low_position):#anlyse modbus's high and low position format returns.
    hex_high = format(int(high_position),'x')
    hex_low = format(int(low_position),'x')
    return int('{}{:0>4}'.format(hex_high,hex_low),16)

def main_baiYe():
    PORT = "/dev/ttyS0"
   #Connect to the slave
    master = modbus_rtu.RtuMaster(
        serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1))#modbus init setting
    master.set_timeout(0.1)
    master.set_verbose(True)

    try:
        return master.execute(2,cst.READ_HOLDING_REGISTERS,500,8)#modbus orderings

    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())


if __name__ == "__main__":
    while True:
        try:
            hum_value,tem_value,_,_,_,ap_value,high_p,low_p = main_baiYe()
            print("air_h:{:.2f},air_t:{:.2f},air_p:{:.2f},illumination:{}".format(float(hum_value)/10,float(tem_value)/10,float(ap_value)/10,dec2hex2dec(high_p,low_p)))
            break

        except Exception as e:
            print(e)

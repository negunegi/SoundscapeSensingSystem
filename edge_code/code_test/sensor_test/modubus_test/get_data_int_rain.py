import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import struct

def dec2hex2dec(high_position,low_position):#anlyse modbus's high and low position format returns.
    hex_high = format(int(high_position),'x')
    hex_low = format(int(low_position),'x')
    return int('{}{:0>4}'.format(hex_high,hex_low),16)

def main_rain():
    PORT = "/dev/ttyS0"
   #Connect to the slave
    master = modbus_rtu.RtuMaster(
        serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1))#modbus init setting
    master.set_timeout(0.1)
    master.set_verbose(True)

    try:
        return master.execute(6,cst.READ_HOLDING_REGISTERS,71,1),\
         master.execute(6,cst.READ_HOLDING_REGISTERS,72,2),\
         master.execute(6,cst.READ_HOLDING_REGISTERS,14,1)#modbus orderings
    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())


if __name__ == "__main__":
    while True:
        try:
            rain_p_tuple,rain_t_tuple,rain_f_tuple = main_rain()
            rain_p, = rain_p_tuple
            rain_t_high,rain_t_low = rain_t_tuple
            print(rain_t_high,rain_t_low)
            rain_f, = rain_f_tuple
            rain_t = dec2hex2dec(rain_t_high,rain_t_low)
            
            print("rain_p:{:.2f},rain_t:{},rain_f:{:.2f}".format(float(rain_p),rain_t,float(rain_f)))
            print("rain_t_finally:{:.2f}".format(((float(rain_p)/100)+1)*rain_t*(float(rain_f)/10000)))
            break

        except Exception as e:
            print(e)
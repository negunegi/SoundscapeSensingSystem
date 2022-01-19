import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import struct

def dec2hex2dec(high_position,low_position):
    hex_high = format(int(high_position),'x')
    hex_low = format(int(low_position),'x')
    return int('{}{:0>4}'.format(hex_high,hex_low),16)

def main_par():
    PORT = "/dev/ttyS0"
   #Connect to the slave
    master = modbus_rtu.RtuMaster(
        serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1))#modbus init setting
    master.set_timeout(0.1)
    master.set_verbose(True)

    try:
        return master.execute(7,cst.READ_HOLDING_REGISTERS,1,2)#modbus orderings
    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())


if __name__ == "__main__":
    # par_tuple = main_par()
    while True:
        try:
            print(main_par())
            par_high,par_low = main_par()
            par = illumination_dec2hex2dec(par_high,par_low)
            print("par:{:.2f}".format(par))
            
            
            # print("rain_p:{:.2f},rain_t:{}{},rain_f:{:.2f},par:{}".format(float(rain_p),rain_t_low,rain_t_high,float(rain_f),par))
            break
        except Exception as e:
            print(e)
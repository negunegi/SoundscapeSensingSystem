from logging import exception
import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import struct

PORT = "/dev/ttyS0"

def main_soil():
    """main"""
    master = modbus_rtu.RtuMaster(
    serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1))#modbus init setting
    master.set_timeout(0.1)
    master.set_verbose(True)

    try:
        #Connect to the slave
        return master.execute(5, cst.READ_HOLDING_REGISTERS, 0, 2)#modbus orderings

    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())

 

if __name__ == "__main__":
    while True:
        try:
            soil_h,soil_t = main_soil()
            print("soil_t:{:.2f},soil_h:{:.2F}".format(float(soil_t)/10,float(soil_h)/10))
            break

        except Exception as e:
            print(e)



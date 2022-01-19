import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import struct

PORT = "/dev/ttyS0"

def readFloat(*args,reverse=False):#anlyse modbus's float format returns.
    for n,m in args:
        m,n = '%04x'%n,'%04x'%m
    if reverse:
        v = n + m
    else:
        v = m + n
    y_bytes = bytes.fromhex(v)
    y = struct.unpack('!f',y_bytes)[0]
    y = round(y,6)
    return y

def main_hourMeter():#get the power of supply sensor data
    """main"""
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=2))#modbus init setting
        master.set_timeout(0.1)
        master.set_verbose(True)

        return readFloat(master.execute(1, cst.READ_HOLDING_REGISTERS, 8192,2)),\
            readFloat(master.execute(1, cst.READ_HOLDING_REGISTERS, 8194,2)),\
            readFloat(master.execute(1, cst.READ_HOLDING_REGISTERS, 16384,2))#modbus orderings

    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())

if __name__ == "__main__":

        while True:
            try:
                ac_v,ac_c,ac_p = main_hourMeter()
                print("ac_v:{:.2f},ac_c:{:.2f},ac_p:{:.2f}".format(float(ac_v),float(ac_c),float(ac_p)))
                break
            except Exception as e:
                print(e)
	
import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import struct

def main_windSpeed():
    PORT = "/dev/ttyS0"
   #Connect to the slave
    # logger = modbus_tk.utils.create_logger("console")
    master = modbus_rtu.RtuMaster(
        serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1))#modbus init setting
    master.set_timeout(0.1)
    master.set_verbose(True)
    # logger.info("connected")

    try:
        return master.execute(4,cst.READ_HOLDING_REGISTERS,0,1)#modbus orderings

    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())

if __name__ == "__main__":
    while True:
        try:
            win_speed, = main_windSpeed()
            print("win_speed:{:.2f}".format(float(win_speed)/10))
            break
        except Exception as e:
            print(e)

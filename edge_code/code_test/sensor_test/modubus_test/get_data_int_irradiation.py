import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import struct

def main_irradiation():
    PORT = "/dev/ttyS0"
   #Connect to the slave
    master = modbus_rtu.RtuMaster(
        serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1))#modbus init setting
    master.set_timeout(0.1)
    master.set_verbose(True)
    try:
        return master.execute(3,cst.READ_HOLDING_REGISTERS,1,1)#modbus orderings

    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())

if __name__ == "__main__":
    while True:
        try:
            irradiation, = main_irradiation()
            print("irradiation:{:.2f}".format(irradiation))
            break

        except Exception as e:
            print(e)

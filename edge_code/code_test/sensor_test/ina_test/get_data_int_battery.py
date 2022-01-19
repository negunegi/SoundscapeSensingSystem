"""Sample code and test for adafruit_in219"""
import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

i2c_bus = board.I2C()
ina1 = INA219(i2c_bus,addr=0x40)
# print("ina219 test")

ina1.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina1.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina1.bus_voltage_range = BusVoltageRange.RANGE_16V

def return_tuple():
    bus_voltage1 = ina1.bus_voltage
    power1 = ina1.power
    current1 = ina1.current
    shunt_voltage1 = ina1.shunt_voltage
    return bus_voltage1+shunt_voltage1,bus_voltage1,current1/1000

if __name__ == "__main__":
    while True:
        bus_voltage1 = ina1.bus_voltage        # voltage on V- (load side)
        shunt_voltage1 = ina1.shunt_voltage    # voltage between V+ and V- across the shunt
        power1 = ina1.power
        current1 = ina1.current                # current in mA
        print("PSU Voltage:{:6.3f}V  Shunt Voltage:{:6.3f}V  Load Voltage:{:6.3f}V  Power:{:6.3f}W  Current:{:6.3f}A".format((bus_voltage1 + shunt_voltage1),(shunt_voltage1),(bus_voltage1),(power1),(current1/1000)))
        time.sleep(0.5)
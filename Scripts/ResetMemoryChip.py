'''
RICOH M320F / SP3710 / P311 TONER CARTRIDGE CHIP RESETTING TOOL (2/2)
by AsdadasRandom

Overwriting

Use this simple script with an ESP32 Board to set the Toner Cartridge Chip to "Full" by
iterating through its 256 bytes and replacing each of them with the information needed for the printer
to recognize the chip as unused (in other words, "7000" prints left or "Full" toner capacity)
'''


import machine
import time
from machine import Pin, I2C

#Connection initialized on two available Pins, but selection can be modified if desired
#The corresponding EEPROM memory operates under a frequency of 100Khz
i2c = I2C(0, scl=Pin(1, Pin.PULL_UP), sda=Pin(8, Pin.PULL_UP), freq=100000)

#Address for the 24c02A EEPROM on the printer chip.
EEPROMaddr = 83 

#Memory dump with the content required for the printer to recognize the chip as "full"
memoryDump_FULL = [b'F', b'\x01', b'\x01', b'\x02', b'\x0e', b'\x01', b'\x01', b'\x00', b'd', b'\x00', b'4', b'0', b'8', b'2', b'8', b'4', b'#', b'\x11', b'R', b'G', b'\x08', b'\x00', b'1', b'X', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'd', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff']

while True:
    
    device = i2c.scan()
    
    #write operation will take place once the chip is connected to the I2C bus accordingly
    #It is advised to check the position of the copper pads in relation to the wires
    if len(device) == 0:
            print("No chip detected")
    else:
        print("Chip detected. Overwriting current memory...")
        time.sleep_ms(500)
            
        #256 bytes will be overwritten at a pace of 8 bits every 5ms, avoid interfering with the connection
        #During the process
        for memPosition in range(0,256,1):
            i2c.writeto_mem(EEPROMaddr, memPosition, memoryDump_FULL[memPosition], addrsize=8)
            time.sleep_ms(5)
        
        print("Memory overwritten succesfully. The chip has been resetted.")
        time.sleep(5)
    
    time.sleep(1)
'''
RICOH M320F / SP3710 / P311 TONER CARTRIDGE CHIP RESETTING TOOL (1/2)
by AsdadasRandom

Reading

Use this simple script with an ESP32 Board to read the content of the EEPROM memory used by the
Toner Cartridge chip and dump it on a list of bytes. This tool compares the content of the memory
with a full-memory dump to see if it is in need of an overwrite.
'''


import machine
import time
from machine import Pin, I2C

#Connection initialized on two available Pins, but selection can be modified if desired
#The corresponding EEPROM memory operates under a frequency of 100Khz
i2c = I2C(0, scl=Pin(1, Pin.PULL_UP), sda=Pin(8, Pin.PULL_UP), freq=100000)

#Address for the 24c02A EEPROM on the printer chip.
EEPROMaddr = 83

#List of 256 elements which will be occuped by the content of the EEPROM memory (256 bytes)
memoryDump = list(range(0,256,1))

#Memory dump with the content required for the printer to recognize the chip as "full"
memoryDump_FULL = [b'F', b'\x01', b'\x01', b'\x02', b'\x0e', b'\x01', b'\x01', b'\x00', b'd', b'\x00', b'4', b'0', b'8', b'2', b'8', b'4', b'#', b'\x11', b'R', b'G', b'\x08', b'\x00', b'1', b'X', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'd', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff', b'\xff']

while True:
    
    device = i2c.scan()
    
    #Read operation will take place once the chip is connected to the I2C bus accordingly
    #It is advised to check the position of the copper pads in relation to the wires
    if len(device) == 0:
            print("No chip detected.")
    else:
        print("Chip detected. Reading its content...")
        time.sleep_ms(500)
        
        #256 bytes will be read rom the EEPROM memory at a rate of 8 bits every 5ms
        #Avoid interfering with the connection during the process
        for memPosition in range(0,256,1):
            memoryDump[memPosition] = i2c.readfrom_mem(EEPROMaddr, memPosition, 1, addrsize=8)
            print("Position number: " +str(memPosition))
            print(memoryDump[memPosition])
            time.sleep_ms(5)
            
        #Once obtained, the content will be shown in a list of 256 bytes objects
        print("The content stored in the chip is as follows: \n")
        print(memoryDump)
        time.sleep(5)
        
        if memoryDump == memoryDump_FULL:
            print("Memory does not need an overwrite")
        else:
            print("Memory needs to be overwritten")
        
    time.sleep(1)
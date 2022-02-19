from machine import Pin, SPI, ADC
import struct
import utime

from nrf24l01 import NRF24L01
                
csn = Pin(15, mode=Pin.OUT, value=1)  
ce  = Pin(14, mode=Pin.OUT, value=0)  
jsy1 = machine.ADC(26) #joystick1 axis y
jsy2 = machine.ADC(27) #joystick2 axis y




pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

def setup():
    nrf = NRF24L01(SPI(0), csn, ce, payload_size=4)

    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])

    return nrf

def demo(nrf): 
    while True:
        xV1 = jsy1.read_u16()
        xV2 = jsy2.read_u16()
        
        s = 0
        if xV1 >= 60000 and xV2 >= 60000 :
            s = 1 # both motors forward
        elif xV1 <= 600 and xV2 <= 600  :
            s = 2 # both motors backwards
        if xV2 >= 60000 and xV1 <= 600 :
            s = 3 # first forward second backwards
        elif xV2 <= 600 and xV1 >= 60000 :
            s = 4 # first motor backwards second forward

        nrf.send(struct.pack("i", s))
        print(s)
        utime.sleep(0.0001)
         


nrf = setup()
demo(nrf)


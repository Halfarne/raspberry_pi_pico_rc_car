from machine import Pin, SPI, ADC, PWM
import struct
import utime

from nrf24l01 import NRF24L01

led = Pin(25, Pin.OUT)                
csn = Pin(15, Pin.OUT, value=1)  
ce  = Pin(14, Pin.OUT, value=0)

jsy1 = machine.ADC(26)
jsx1 = machine.ADC(27)

m1p1 = Pin(18, Pin.OUT) #motor1 frontwards
m1p2 = Pin(19, Pin.OUT) #motor1 backwards
m2p1 = Pin(20, Pin.OUT) #motor2 frontwards
m2p2 = Pin(21, Pin.OUT) #motor2 backwards
m1e = Pin(16, Pin.OUT) #motor1 enabled
m2e = Pin(17, Pin.OUT) #motor2 enabled

pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")
m1e(1)
m2e(1)

def setup():
    nrf = NRF24L01(SPI(0), csn, ce, payload_size=4)

    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    led.value(0)
    return nrf

def demo(nrf):
    while True:
        
        if nrf.any():
            buf = nrf.recv()
            got = struct.unpack("i", buf)[0]
            print("rx", got)
            if got == 2 :
                print("dopredu")
                m1p1(1)
                m2p1(1)
            if got == 1 :
                print("dozadu")
                m1p2(1)
                m2p2(1)
            if got == 4 :
                print("doprava")
                m1p1(1)
                m2p2(1)
            if got == 3 :
                print("doleva")
                m2p2(1)
                m1p1(1)
            if got == 0:
                m1p1(0)
                m1p2(0)
                m2p1(0)
                m2p2(0)


nrf = setup()
demo(nrf)


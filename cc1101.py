#!/usr/bin/env python3

'''
MIT License

Copyright (c) 2020 Alinux

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import time, struct, wiringpi, datetime

SS_PIN = 10 # WiringPi GPIO => corresponds to GPIO 8
GDO0 = 6 # WiringPi GPIO => corresponds to GPIO 25
GDO2 = 99 # unused

F_915 = 0x00
F_433 = 0x01
F_868 = 0x02

F2_868 = 0x21 # Carrier frequency = 868 MHz
F1_868 = 0x62 # Carrier frequency = 868 MHz
F0_868 = 0x76 # Carrier frequency = 868 MHz
F2_915 = 0x22 # Carrier frequency = 902 MHz
F1_915 = 0xB1 # Carrier frequency = 902 MHz
F0_915 = 0x3B # Carrier frequency = 902 MHz
F2_433 = 0x10 # Carrier frequency = 433 MHz
F1_433 = 0xA7 # Carrier frequency = 433 MHz
F0_433 = 0x62 # Carrier frequency = 433 MHz

CC1101_IOCFG2 = 0x00 # GDO2 output pin configuration
CC1101_IOCFG1 = 0x01 # GDO1 output pin configuration
CC1101_IOCFG0 = 0x02 # GDO0 output pin configuration
CC1101_FIFOTHR = 0x03 # RX FIFO and TX FIFO thresholds
CC1101_SYNC1 = 0x04 # Sync word, high INT8U
CC1101_SYNC0 = 0x05 # Sync word, low INT8U
CC1101_PKTLEN = 0x06 # Packet length
CC1101_PKTCTRL1 = 0x07 # Packet automation control
CC1101_PKTCTRL0 = 0x08 # Packet automation control
CC1101_ADDR = 0x09 # Device address
CC1101_CHANNR = 0x0A # Channel number
CC1101_FSCTRL1 = 0x0B # Frequency synthesizer control
CC1101_FSCTRL0 = 0x0C # Frequency synthesizer control
CC1101_FREQ2 = 0x0D # Frequency control word, high INT8U
CC1101_FREQ1 = 0x0E # Frequency control word, middle INT8U
CC1101_FREQ0 = 0x0F # Frequency control word, low INT8U
CC1101_MDMCFG4 = 0x10 # Modem configuration
CC1101_MDMCFG3 = 0x11 # Modem configuration
CC1101_MDMCFG2 = 0x12 # Modem configuration
CC1101_MDMCFG1 = 0x13 # Modem configuration
CC1101_MDMCFG0 = 0x14 # Modem configuration
CC1101_DEVIATN = 0x15 # Modem deviation setting
CC1101_MCSM2 = 0x16 # Main Radio Control State Machine configuration
CC1101_MCSM1 = 0x17 # Main Radio Control State Machine configuration
CC1101_MCSM0 = 0x18 # Main Radio Control State Machine configuration
CC1101_FOCCFG = 0x19 # Frequency Offset Compensation configuration
CC1101_BSCFG = 0x1A # Bit Synchronization configuration
CC1101_AGCCTRL2 = 0x1B # AGC control
CC1101_AGCCTRL1 = 0x1C # AGC control
CC1101_AGCCTRL0 = 0x1D # AGC control
CC1101_WOREVT1 = 0x1E # High INT8U Event 0 timeout
CC1101_WOREVT0 = 0x1F # Low INT8U Event 0 timeout
CC1101_WORCTRL = 0x20 # Wake On Radio control
CC1101_FREND1 = 0x21 # Front end RX configuration
CC1101_FREND0 = 0x22 # Front end TX configuration
CC1101_FSCAL3 = 0x23 # Frequency synthesizer calibration
CC1101_FSCAL2 = 0x24 # Frequency synthesizer calibration
CC1101_FSCAL1 = 0x25 # Frequency synthesizer calibration
CC1101_FSCAL0 = 0x26 # Frequency synthesizer calibration
CC1101_RCCTRL1 = 0x27 # RC oscillator configuration
CC1101_RCCTRL0 = 0x28 # RC oscillator configuration
CC1101_FSTEST = 0x29 # Frequency synthesizer calibration control
CC1101_PTEST = 0x2A # Production test
CC1101_AGCTEST = 0x2B # AGC test
CC1101_TEST2 = 0x2C # Various test settings
CC1101_TEST1 = 0x2D # Various test settings
CC1101_TEST0 = 0x2E # Various test settings
CC1101_SRES = 0x30 # Reset chip.
CC1101_SFSTXON = 0x31 # Enable and calibrate frequency synthesizer (if MCSM0.FS_AUTOCAL=1).
                      # If in RX/TX: Go to a wait state where only the synthesizer is running (for quick RX / TX turnaround).
CC1101_SXOFF = 0x32 # Turn off crystal oscillator.
CC1101_SCAL = 0x33 # Calibrate frequency synthesizer and turn it off (enables quick start).
CC1101_SRX = 0x34 # Enable RX. Perform calibration first if coming from IDLE and MCSM0.FS_AUTOCAL=1.
CC1101_STX = 0x35 # In IDLE state: Enable TX. Perform calibration first if
                  # MCSM0.FS_AUTOCAL=1. If in RX state and CCA is enabled: only go to TX if channel is clear.
CC1101_SIDLE = 0x36 # Exit RX / TX, turn off frequency synthesizer and exit. Wake-On-Radio mode if applicable.
CC1101_SAFC = 0x37 # Perform AFC adjustment of the frequency synthesizer
CC1101_SWOR = 0x38 # Start automatic RX polling sequence (Wake-on-Radio)
CC1101_SPWD = 0x39 # Enter power down mode when CSn goes high.
CC1101_SFRX = 0x3A # Flush the RX FIFO buffer.
CC1101_SFTX = 0x3B # Flush the TX FIFO buffer.
CC1101_SWORRST = 0x3C # Reset real time clock.
CC1101_SNOP = 0x3D # No operation. May be used to pad strobe commands to two INT8Us for simpler software.
CC1101_PARTNUM = 0x30
CC1101_VERSION = 0x31
CC1101_FREQEST = 0x32
CC1101_LQI = 0x33
CC1101_RSSI = 0x34
CC1101_MARCSTATE = 0x35
CC1101_WORTIME1 = 0x36
CC1101_WORTIME0 = 0x37
CC1101_PKTSTATUS = 0x38
CC1101_VCO_VC_DAC = 0x39
CC1101_TXBYTES = 0x3A
CC1101_RXBYTES = 0x3B
CC1101_PATABLE = 0x3E
CC1101_TXFIFO = 0x3F
CC1101_RXFIFO = 0x3F

WRITE_SINGLE_BYTE = 0x00 # write single
WRITE_BURST = 0x40 # write burst
READ_SINGLE_BYTE = 0x80 # read single
READ_BURST = 0xC0 # read burst
BYTES_IN_RXFIFO = 0x7F # byte number in RXfifo

class Cc1101(object):

    def __init__(self, carrier=F_433, callback=None):
        self.carrier = carrier
        self.callback = (lambda x:None) if callback is None else callback
        wiringpi.wiringPiSetup()
        wiringpi.wiringPiSPISetupMode(0, 4000000, 0) # spi initialization
        wiringpi.pinMode(GDO0, wiringpi.INPUT)
        wiringpi.pinMode(GDO2, wiringpi.INPUT)
        self.reset() # CC1101 reset
        self.regConfigSettings(self.carrier) # CC1101 register config
        self.spiWriteBurstReg(CC1101_PATABLE, (0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60)) # CC1101 PATABLE config
        wiringpi.pinMode(GDO0, wiringpi.GPIO.INPUT)
        wiringpi.pullUpDnControl(GDO0, wiringpi.GPIO.PUD_UP)
        wiringpi.wiringPiISR(GDO0, wiringpi.GPIO.INT_EDGE_FALLING, lambda:self.callback(buffer=self.receiveData()))

    def reset(self):
        wiringpi.digitalWrite(SS_PIN, wiringpi.LOW)
        wiringpi.delayMicroseconds(10)
        wiringpi.digitalWrite(SS_PIN, wiringpi.HIGH)
        wiringpi.delayMicroseconds(40)
        self.spiStrobe(CC1101_SRES)
        wiringpi.delay(1)

    def spiWriteReg(self, addr=None, value=None):
        wiringpi.wiringPiSPIDataRW(0, bytes([addr|WRITE_SINGLE_BYTE, value]))

    def spiWriteBurstReg(self, addr=None, buffer=None):
        wiringpi.wiringPiSPIDataRW(0, bytes([addr|WRITE_BURST]+list(buffer)))

    def spiStrobe(self, strobe=None):
        wiringpi.wiringPiSPIDataRW(0, bytes([strobe, 0]))

    def spiReadReg(self, addr=None):
        len, data = wiringpi.wiringPiSPIDataRW(0, bytes([addr|READ_SINGLE_BYTE, 0]))
        return data[1]

    def spiReadBurstReg(self, addr=None, num=None):
        len, data = wiringpi.wiringPiSPIDataRW(0, bytes([addr|READ_BURST] + num*[0]))
        return data[1:]

    def spiReadStatus(self, addr=None):
        len, data = wiringpi.wiringPiSPIDataRW(0, bytes([addr | READ_BURST, 0]))
        return data[1]

    def regConfigSettings(self, f=None):
        self.spiWriteReg(CC1101_FSCTRL1, 0x08)
        self.spiWriteReg(CC1101_FSCTRL0, 0x00)
        if f == F_868:
          	self.spiWriteReg(CC1101_FREQ2, F2_868)
          	self.spiWriteReg(CC1101_FREQ1, F1_868)
          	self.spiWriteReg(CC1101_FREQ0, F0_868)
        elif f ==  F_915:
            self.spiWriteReg(CC1101_FREQ2, F2_915)
            self.spiWriteReg(CC1101_FREQ1, F1_915)
            self.spiWriteReg(CC1101_FREQ0, F0_915)
        elif f == F_433:
            self.spiWriteReg(CC1101_FREQ2, F2_433)
            self.spiWriteReg(CC1101_FREQ1, F1_433)
            self.spiWriteReg(CC1101_FREQ0, F0_433)
        else:
            pass

        self.spiWriteReg(CC1101_MDMCFG4, 0x5B)
        self.spiWriteReg(CC1101_MDMCFG3, 0xF8)
        self.spiWriteReg(CC1101_MDMCFG2, 0x03)
        self.spiWriteReg(CC1101_MDMCFG1, 0x22)
        self.spiWriteReg(CC1101_MDMCFG0, 0xF8)
        self.spiWriteReg(CC1101_CHANNR, 0x00)
        self.spiWriteReg(CC1101_DEVIATN, 0x47)
        self.spiWriteReg(CC1101_FREND1, 0xB6)
        self.spiWriteReg(CC1101_FREND0, 0x10)
        self.spiWriteReg(CC1101_MCSM0, 0x18)
        self.spiWriteReg(CC1101_FOCCFG, 0x1D)
        self.spiWriteReg(CC1101_BSCFG, 0x1C)
        self.spiWriteReg(CC1101_AGCCTRL2, 0xC7)
        self.spiWriteReg(CC1101_AGCCTRL1, 0x00)
        self.spiWriteReg(CC1101_AGCCTRL0, 0xB2)
        self.spiWriteReg(CC1101_FSCAL3, 0xEA)
        self.spiWriteReg(CC1101_FSCAL2, 0x2A)
        self.spiWriteReg(CC1101_FSCAL1, 0x00)
        self.spiWriteReg(CC1101_FSCAL0, 0x11)
        self.spiWriteReg(CC1101_FSTEST, 0x59)
        self.spiWriteReg(CC1101_TEST2, 0x81)
        self.spiWriteReg(CC1101_TEST1, 0x35)
        self.spiWriteReg(CC1101_TEST0, 0x09)
        self.spiWriteReg(CC1101_IOCFG2, 0x0B) # serial clock.synchronous to the data in synchronous serial mode
        self.spiWriteReg(CC1101_IOCFG0, 0x06) # asserts when sync word has been sent/received, and de-asserts at the end of the packet 
        self.spiWriteReg(CC1101_PKTCTRL1, 0x04) # two status bytes will be appended to the payload of the packet,including RSSI LQI and CRC OK No address check
        self.spiWriteReg(CC1101_PKTCTRL0, 0x05) # whitening off, CRC Enable variable length packets, packet length configured by the first byte after sync word
        self.spiWriteReg(CC1101_ADDR, 0x00) # address used for packet filtration.
        self.spiWriteReg(CC1101_PKTLEN, 0x3D) # 61 bytes max length

    def sendData(self, txBuffer=None, size=None):
        self.spiWriteReg(CC1101_TXFIFO, size)
        self.spiWriteBurstReg(CC1101_TXFIFO, txBuffer, size) # write data to send
        self.spiStrobe(CC1101_STX) # start send	
        while not wiringpi.digitalRead(GDO0):
            pass # Wait for GDO0 to be set -> sync transmitted  
        while digitalRead(GDO0):
            pass # Wait for GDO0 to be cleared -> end of packet
        self.spiStrobe(CC1101_SFTX) # flush TX FIFO

    def setReceive(self):
    	self.spiStrobe(CC1101_SRX)

    def receiveData(self):
        rxBuffer = []
        if(self.spiReadStatus(CC1101_RXBYTES) & BYTES_IN_RXFIFO):
            size = self.spiReadReg(CC1101_RXFIFO)
            rxBuffer = self.spiReadBurstReg(CC1101_RXFIFO, size)
        self.spiStrobe(CC1101_SFRX) # flush the buffer
        self.setReceive() # put it in receive mode again
        return rxBuffer # packet size

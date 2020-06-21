# py1101
Python3 port of the Simon Monks' clone of the ELECHOUSE_CC1101 C++ library, https://github.com/simonmonk/CC1101_arduino.
The CC1101 module is described here: http://www.elechouse.com/elechouse/images/product/CC1101%20Wirless%20Data%20Transmittion%20Module/CC1101%20Module%20Manual.pdf 

# How to connect the CC1101 to the Raspberry?

|Raspberry|CC1101|
|---------|------|
|GND|GND|
|3.3V|VCC|
|GPIO 8|CSN/SS|
|GPIO 10|SI/MOSI|
|GPIO 9|SO/MISO|
|GPIO 11|SCK|
|GPIO 25|GD0|

# How to install the library?

Before everything else, you need to be sure that the SPI interface is enabled on your Raspberry.

Then, you install wiringpi (http://wiringpi.com). There is already a Python package for that:
```
sudo pip3 wiringpi
```

# Simple Python program to receive data

```
#!/usr/bin/env python3
import time
from cc1101 import Cc1101

# function that is called when receiving a buffer
def onReceive(buffer):
    # print the content of the buffer in hexa
    print(' '.join([hex(x)[2:].zfill(2) for x in buffer]))

if __name__ == '__main__':
    # create an instance by defining a callback, then set CC1101 in receive mode
    Cc1101(callback=onReceive).setReceive()
    # wait loop
    while True: time.sleep(999)
```

# Caveats

Wiringpi is deprecated (http://wiringpi.com/wiringpi-deprecated).

# License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2F10git%2Fpy1101.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2F10git%2Fpy1101?ref=badge_large)

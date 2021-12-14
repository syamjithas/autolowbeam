import _thread
import machine
from machine import ADC, Pin
from time import sleep


lightValue = 0
threshold = 50
mode = 1
modeCount = 0
photoPIN = 26
relayYellow = machine.Pin(13, machine.Pin.OUT)
relayWhite = machine.Pin(14, machine.Pin.OUT)
button = machine.Pin(15, machine.Pin.IN)
inbuiltled = Pin(25, Pin.OUT)
relayWhite.high()
relayYellow.high()

second_thread = True
baton = _thread.allocate_lock()


def readLight():
    photoRes = ADC(Pin(photoPIN))
    lightValue = photoRes.read_u16()
    lightValue = round(lightValue / 65535 * 100, 2)
    return lightValue


def highautoModeLightControl():
    #print("highautoModeLightControl")
    while True:
        if second_thread == False:
            #print("highautoModeLightControl exit")
            _thread.exit()
        lightIntencity = readLight()
        if lightIntencity < threshold:
            relayWhite.low()
            sleep(0.5)
        elif lightIntencity > threshold:
            relayWhite.high()
            sleep(1)
            


def lowautoModeLightControl():
    #print("lowautoModeLightControl")
    while True:
        if second_thread == False:
            #print("lowautoModeLightControl exit")
            _thread.exit()
        lightIntencity = readLight()
        if lightIntencity < threshold:
            relayYellow.low()
            sleep(0.5)
        elif lightIntencity > threshold:
            relayYellow.high()
            sleep(1)


def autohighlowModeLightControl():
    #print("autohighlowModeLightControl")
    while True:
        if second_thread == False:
            #print("autohighlowModeLightControl exit")
            _thread.exit()
        lightIntencity = readLight()
        if lightIntencity < threshold:
            relayYellow.high()
            relayWhite.low()
            sleep(0.5)
        elif lightIntencity > threshold:
            relayWhite.high()
            relayYellow.low()
            sleep(1)
            


def highautoMode():
    #print("highautoMode")
    sleep(0.5)
    relayWhite.low()
    sleep(0.5)
    relayWhite.high()
    sleep(0.5)
    relayWhite.low()
    _thread.start_new_thread(highautoModeLightControl, ())


def highMode():
    #print("highMode")
    sleep(0.5)
    relayWhite.low()
    sleep(0.5)
    relayWhite.high()
    sleep(0.5)
    relayWhite.low()
    sleep(0.5)
    relayWhite.high()
    sleep(0.5)
    relayWhite.low()


def lowautoMode():
    #print("lowautoMode")
    sleep(0.5)
    relayYellow.low()
    sleep(0.5)
    relayYellow.high()
    sleep(0.5)
    relayYellow.low()
    _thread.start_new_thread(lowautoModeLightControl, ())


def lowMode():
    #print("lowMode")
    sleep(0.5)
    relayYellow.low()
    sleep(0.5)
    relayYellow.high()
    sleep(0.5)
    relayYellow.low()
    sleep(0.5)
    relayYellow.high()
    sleep(0.5)
    relayYellow.low()


def autohighlowMode():
    #print("autohighlowMode")
    sleep(0.5)
    relayWhite.low()
    sleep(0.5)
    relayWhite.high()
    relayYellow.low()
    sleep(0.5)
    relayYellow.high()
    relayWhite.low()
    sleep(0.5)
    relayWhite.high()
    relayYellow.low()
    sleep(0.5)
    relayYellow.high()
    relayWhite.low()
    _thread.start_new_thread(autohighlowModeLightControl, ())


def modefn():
    relayYellow.high()
    relayWhite.high()
    if mode == 1:
        highautoMode()
    elif mode == 2:
        highMode()
    elif mode == 3:
        lowautoMode()
    elif mode == 4:
        lowMode()
    elif mode == 5:
        autohighlowMode()


# init
modefn()

while True:
    if button.value():
        modeCount += 1
        if modeCount == 100:
            modeCount = 0
            mode = 1 if mode == 5 else mode + 1
            inbuiltled.high()
            second_thread = False
            #print(second_thread)
            sleep(1.5)
            second_thread = True
            #print(second_thread)
            modefn()
            sleep(1)
    else:
        modeCount = 0
        inbuiltled.low()
        

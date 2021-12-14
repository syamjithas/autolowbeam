import _thread
import machine
from machine import ADC, Pin
from time import sleep


lightValue = 0
threshold = 50
mode = 0
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
    # print("highautoModeLightControl")
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
            sleep(0.9)


def lowautoModeLightControl():
    # print("lowautoModeLightControl")
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
            sleep(0.9)


def autohighlowModeLightControl():
    # print("autohighlowModeLightControl")
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
            sleep(0.9)


def highautoMode():
    # print("highautoMode")
    relayWhite.low()
    _thread.start_new_thread(highautoModeLightControl, ())


def highMode():
    # print("highMode")
    relayWhite.low()


def lowautoMode():
    # print("lowautoMode")
    _thread.start_new_thread(lowautoModeLightControl, ())


def lowMode():
    # print("lowMode")
    relayYellow.low()


def autohighlowMode():
    # print("autohighlowMode")
    relayWhite.low()
    _thread.start_new_thread(autohighlowModeLightControl, ())


def modefn():
    if mode == 0:
        relayYellow.high()
        relayWhite.high()
    elif mode == 1:
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
            relayYellow.low()
            relayWhite.high()
            modeCount = 0
            mode = 0 if mode == 5 else mode + 1
            inbuiltled.high()
            second_thread = False
            # print(second_thread)
            sleep(0.5)
            relayYellow.high()
            sleep(0.5)
            second_thread = True
            # print(second_thread)
            modefn()
            sleep(1)
    else:
        modeCount = 0
        inbuiltled.low()


import machine
import time
import random
import micropython_dotstar as dotstar
import helper as helpe
from machine import Pin, SPI
from machine import Timer
import _thread
import utime

machine.freq(240000000)

# On-board DotStar for the TinyPICO

spi = SPI(0, sck=Pin(18), mosi=Pin(19), miso=Pin(4))  # Configure SPI - note: miso is unused
dots = dotstar.DotStar(spi, 10, brightness=0.8)
tracks = helpe.Helper
buttonDown = Pin(16, Pin.IN, Pin.PULL_DOWN)
buttonUp = Pin(17, Pin.IN, Pin.PULL_DOWN)
buttonSel = Pin(18, Pin.IN, Pin.PULL_DOWN)

# Using a DotStar Digital LED Strip with 30 LEDs connected to SPI
# dots = dotstar.DotStar(spi=SPI(sck=Pin(x), mosi=Pin(y)), 30, brightness=0.2)

# HELPERS

backward = bool(0)
trackNumber = 2
trackPlaying = bool(1)

currentTrack = tracks._getTrackFromNumber(3)

updateMenu = bool(1)
numOfLed = 12



waittime = 0
count =0






def random_color():
    return random.randrange(0, 7) * 32


def playTrack(track):
    x = 0
    start = time.ticks_ms()
    c = time.ticks_ms()
    d = 0
    for i in track:

        if x >= numOfLed:
            if trackPlaying == bool(1):

                x = 0
                time.sleep_ms(1)
                dots.show()

               # print(50-start)

                start = 0
            else:

                return

        dots._set_item(x, i)

        x += 1


def plusTrackNumber():
    trackNumber += 1


def minusTrackNumber():
    trackNumber -= 1


maxTrack = 30


def SelButton(pin):
    buttonSel.irq(handler=None)

    time.sleep_ms(175)

    buttonSel.irq(handler=SelButton)

    global trackPlaying
    global updateMenu
    trackPlaying = not trackPlaying
   
    updateMenu = bool(1)


def UpButton(pin):

    buttonUp.irq(handler=None)

    time.sleep_ms(175)

    buttonUp.irq(handler=UpButton)

    global updateMenu
    global trackNumber
    trackNumber += 1
    print('Track Up')
    updateMenu = bool(1)


def DownButton(pin):
    buttonDown.irq(handler=None)

    time.sleep_ms(175)

    buttonDown.irq(handler=DownButton)

    global updateMenu
    global trackNumber
    if trackNumber <= 0:
        trackNumber = maxTrack + 1
    trackNumber -= 1
    print('track Down')
    updateMenu = bool(1)


def upDateMunuDots():

    i = 0
    x = 0
    menuPageCounter = 0
    while i < trackNumber:
        if x >= numOfLed:
            x = 0
            menuPageCounter += 1
        if menuPageCounter <= 0:
            dots._set_item(x, (0, 150, 0))
        if menuPageCounter == 1:
            dots._set_item(x, (0, 150, 255))

        i += 1
        x += 1
    h = x
    while h < numOfLed:
        dots._set_item(h, (0, 0, 0))
        h += 1

    dots._set_item(x, (225, 0, 0))
    dots.show()


# timer = Timer().init(period=1, mode=Timer.PERIODIC,tick_hz=12, callback=lambda t:BUTTONCHECK())

SelButtonActive = bool(0)
UpButtonActive = bool(0)
DownButtonActive = bool(0)

buttonSel.irq(SelButton, Pin.IRQ_FALLING)
buttonUp.irq(UpButton, Pin.IRQ_FALLING)
buttonDown.irq(DownButton, Pin.IRQ_FALLING)
tracks.lastTrack = 0;
# MAIN LOOP

while True:



    if tracks.GetCurrentTrackNumber() == currentTrack:
        currentTrack = currentTrack
    else:
        currentTrack = tracks._getTrackFromNumber(trackNumber)

    if trackPlaying == bool(1):
        playTrack(currentTrack)

    if trackPlaying == bool(0):
        if updateMenu == bool(1):
            upDateMunuDots()

            updateMenu = bool(0)



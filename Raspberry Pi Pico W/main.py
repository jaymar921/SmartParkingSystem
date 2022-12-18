from machine import Pin, UART
from time import sleep
import modules.ParkingLogics as ParkingLogics
from modules.mfrc522 import MFRC522
import utime
import _thread
from modules.gpio_lcd import GpioLcd
from modules.CLASSES import Card


rfid_reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

#bluetooth_module = UART(0, 9600)



# 1068049966 3118564713 '63914259'
# GLOBAL VARIABLES
SYSTEM_TIME = '0'
TAPPED: bool = False
REGISTERED_CARDS: list = [Card('1068049966', 23), Card('3118564713', 50.25)]
PARKED: list = []
RELOAD: bool = False

def clock():
    global SYSTEM_TIME
    global TAPPED
    global PARKED
    minute = 0
    hour = 11
    day_night = 'AM'
    day_night_flipper = 0
    tap_sec_del = 0
    while True:
        utime.sleep(1)
        minute = minute + 1
        if minute == 60:
            hour = hour + 1
            minute = 0
            # Update the time of parked cars
            for p in PARKED:
                p.time_parked = p.time_parked + 1
        if hour > 12:
            hour = 1
            day_night_flipper = 0
        if hour == 12 and day_night_flipper == 0:
            day_night_flipper = 1
            if 'AM' in day_night:
                day_night = 'PM'
            else:
                day_night = 'AM'
        
        SYSTEM_TIME = str(f"{hour:02d}:{minute:02d} {day_night}")
        if TAPPED:
            tap_sec_del = tap_sec_del + 1
            if tap_sec_del >= 7:
                tap_sec_del = 0
                TAPPED = False
        else:    
            ParkingLogics.displayTime(SYSTEM_TIME)
 
def reader():
    global SYSTEM_TIME
    global TAPPED
    global REGISTERED_CARDS
    global RELOAD
    while True:
        #bluetooth_listen()
        rfid_reader.init()
        
        
        if TAPPED:
            continue
        
        cardId = getCardID()
        
        if cardId == '':
            continue
        
        if RELOAD:
            ParkingLogics.reloadCard(REGISTERED_CARDS, cardId)
            RELOAD = False
            TAPPED = True
            continue
        
        if '63914259' == cardId:
            RELOAD = True
            ParkingLogics.displayLCD("Tap a card to","reload...")
            TAPPED = True
            continue
            
        
        print("CARD ID: "+str(cardId))
        TAPPED = True
        ParkingLogics.onTap(PARKED, REGISTERED_CARDS, SYSTEM_TIME, cardId)
        
                

#def bluetooth_listen():
#    if bluetooth_module.any():
#        command = str(bluetooth_module.readline())
#        print(command)

#_thread.start_new_thread(main, ())

def getCardID() -> str:
    (stat, tag_type) = rfid_reader.request(rfid_reader.REQIDL)
    if stat == rfid_reader.OK:
        (stat, uid) = rfid_reader.SelectTagSN()
        if stat == rfid_reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            return str(card)
    return ''

_thread.start_new_thread(clock, ())
reader()




#main()
from machine import Pin, PWM
from modules.CLASSES import Card
from gpio_lcd import GpioLcd
import utime

lcd = GpioLcd(rs_pin = Pin(8),
    enable_pin = Pin(9),
    d4_pin = Pin(10),
    d5_pin = Pin(11),
    d6_pin = Pin(12),
    d7_pin = Pin(13),
    num_lines = 2,
    num_columns = 16)

MID = 1_500_000
MIN = 1_000_000
MAX = 2_000_000

servo = PWM(Pin(15))
servo.freq(50)
servo.duty_ns(MID)


def onTap(PARKED, REGISTERED_CARDS, time: str,uid: str):
    for CARD in REGISTERED_CARDS:
        if CARD.uid == uid:
            # Check if the car is already parked
            if carParked(PARKED, CARD):
                time_parked = CARD.time_parked - 2
                payment = time_parked * 5 # P5 for each Hour
                if CARD.balance >= 20:
                    if CARD.time_parked <= 2:
                        PARKED.remove(CARD)
                        displayLCD("Thank you :D","Come back again")
                        print('OFF PARKING AT '+time)
                        openGate()
                        utime.sleep(3)
                        closeGate()
                        displayLCD("Card Balance","P"+str(CARD.balance))
                        CARD.time_parked = -1
                    else:
                        PARKED.remove(CARD)
                        CARD.balance = CARD.balance - payment
                        displayLCD(f"Paid P{payment}","Balance: P"+str(CARD.balance))
                        print('OFF PARKING AT '+time)
                        openGate()
                        utime.sleep(3)
                        closeGate()
                        displayLCD("Card Balance","P"+str(CARD.balance))
                        CARD.time_parked = -1
                elif CARD.balance >= payment:
                    if CARD.time_parked <= 2:
                        PARKED.remove(CARD)
                        displayLCD("Thank you :D","Come back again")
                        print('OFF PARKING AT '+time)
                        openGate()
                        utime.sleep(3)
                        closeGate()
                        displayLCD("Please reload","your card")
                        utime.sleep(2)
                        displayLCD("Card Balance","P"+str(CARD.balance))
                        CARD.time_parked = -1
                    else:
                        PARKED.remove(CARD)
                        CARD.balance = CARD.balance - payment
                        displayLCD("Paid P{payment}","Balance: P"+str(CARD.balance))
                        print('OFF PARKING AT '+time)
                        openGate()
                        utime.sleep(3)
                        closeGate()
                        displayLCD("Please reload","your card")
                        utime.sleep(2)
                        displayLCD("Card Balance","P"+str(CARD.balance))
                        CARD.time_parked = -1
                else:
                    displayLCD("Not enough","balance")
            else:
                # If going to park, check balance
                if CARD.balance >= 20: 
                    CARD.balance = CARD.balance - 10
                    displayLCD("Paid P10","Balance: P"+str(CARD.balance))
                    CARD.time_parked = 0
                    PARKED.append(CARD)
                    print('CAR PARKED AT '+time)
                    openGate()
                    utime.sleep(3)
                    closeGate()
                elif CARD.balance > 10:
                    CARD.balance = CARD.balance - 10
                    displayLCD("Paid P10","Balance: P"+str(CARD.balance))
                    openGate()
                    utime.sleep(3)
                    closeGate()
                    displayLCD("Please reload","your card")
                    CARD.time_parked = 0
                    PARKED.append(CARD)
                    print('CAR PARKED AT '+time)
                else:
                    displayLCD("Not enough","balance")
                return
            return
    REGISTERED_CARDS.append(Card(uid, 0.0))
    print(f"Registered {uid}")
    displayLCD("New Card","Registered")
def displayTime(time):
    lcd.clear()
    lcd.putstr("Time: "+str(time))
    

def carParked(PARKED, CARD) -> bool:
    for P in PARKED:
        if P.uid == CARD.uid:
            return True
    return False

def reloadCard(REGISTERED_CARDS, uid):
    for CARD in REGISTERED_CARDS:
        if CARD.uid == uid:
            CARD.balance = CARD.balance + 20.0
            print("Loaded P20 to CARD: "+uid)
            displayLCD("Loaded P20.0",f"Balance P{CARD.balance}")
            break
    

def displayLCD(str1, str2):
    lcd.clear()
    lcd.putstr(str1)
    lcd.move_to(0,1)
    lcd.putstr(str2)
    
def openGate():
    servo.duty_ns(MIN)

def closeGate():
    servo.duty_ns(MID)
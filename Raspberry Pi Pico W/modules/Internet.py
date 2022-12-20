import network
import secrets
import urequests
import time
import ujson as json


def Connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    return wlan.isconnected()

def getCards():
    if Connect():
        cards = urequests.get('http://203.177.71.218:8000/api/cards').json()
        return cards
    return None

def updateCard(data):
    if Connect():
        data = json.dumps(data)
        cards = urequests.put('http://203.177.71.218:8000/api/cards', headers = {'content-type': 'application/json'}, data=data)
        return cards
    return None

def registerCard(data):
    if Connect():
        data = json.dumps(data)
        cards = urequests.post('http://203.177.71.218:8000/api/cards', headers = {'content-type': 'application/json'}, data=data)
        return cards
    return None

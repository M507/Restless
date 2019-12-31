"""
Config valuables.

NOTE: I recommend changing the values of:
    the IDentifier and SHIFT
    then make sure to change them also in the implant code.
"""


# Static values
BLUE_TEAM_INTERFACE = "utun1"
IDentifier = "xXQ"
SHIFT = 1

# Debug mode
debug = 1

# icmp.h
ICMP_ECHO_REQUEST = 8
ICMP_Time_Exceeded = 11
CHOSEN_TYPE = ICMP_Time_Exceeded

listOfIPs = []

ERROR_DESCR = {
    1: ' - Note that ICMP messages can only be '
       'sent from processes running as root.',
    10013: ' - Note that ICMP messages can only be sent by'
           ' users or processes with administrator rights.'
}

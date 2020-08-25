"""
Pure ICMPLike implementation using raw socket with Caesar cipher

Authors: Mohammed and Chris.
Author's website: Mohad.red
Thanks to Chris hallman, https://mail.python.org/pipermail/tutor/2009-November/072707.html
"""

import time, socket, struct, select, asyncore, random
from Config import *
from Common import *

ICMP_CODE = socket.getprotobyname('icmp')

"""
Sends one pkt to the given "dest_addr" which can be an ip or hostname.
"timeout" can be any integer or float except negatives and zero.
"count" specifies how many pings will be sent.
Displays the result on the screen.

"""
def SendIt(dest_addr,command, timeout=2, count=1):
    for i in range(count):
        print('Poking ({})'.format(dest_addr))
        delay = do_one(dest_addr, command, timeout)
        if delay == None:
            pass
            #print('failed. (Timeout within {} seconds.)'.format(timeout))
        else:
            delay = round(delay * 1000.0, 4)
            #print('get ping in {} milliseconds.'.format(delay))
    print("")

def checksum(source_string):
    sum = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        this_val = ord(source_string[count + 1]) * 256 + ord(source_string[count])
        sum = sum + this_val
        sum = sum & 0xffffffff  # Necessary?
        count = count + 2
    if count_to < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff  # Necessary?
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


"""
Create a new echo request packet based on the given "id".
"""
def create_packet(id, command):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    header = struct.pack('bbHHh', CHOSEN_TYPE, 0, 0, id, 1)
    data = fix(command,500)
    data = command
    # Encrypt
    data = shift(data, SHIFT)
    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)
    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack('bbHHh', CHOSEN_TYPE, 0,
                         socket.htons(my_checksum), id, 1)
    return header + data

"""
Sends one ping to the given "dest_addr" which can be an ip or hostname.
"timeout" can be any integer or float except negatives and zero.
Returns either the delay (in seconds) or None on timeout and an invalid
address, respectively.
"""
def do_one(dest_addr,command, timeout=1):
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
    except socket.error as e:
        if e.errno in ERROR_DESCR:
            # Operation not permitted
            raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
        raise  # raise the original error
    try:
        host = socket.gethostbyname(dest_addr)
    except socket.gaierror:
        return
    # we have to make sure that our packet id is not greater than 65535.
    packet_id = int((id(timeout) * random.random()) % 65535)
    packet = create_packet(packet_id, command)
    while packet:
        # The icmp protocol does not use a port, but the function
        # below expects it, so we can give it any port.
        sent = my_socket.sendto(packet, (dest_addr, 1))
        packet = packet[sent:]
    delay = receiveIt(my_socket, packet_id, time.time(), timeout)
    my_socket.close()
    return delay


def receiveIt(my_socket, packet_id, time_sent, timeout):
    # Receive the ping from the socket.
    time_left = timeout
    while True:
        started_select = time.time()
        ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = time.time() - started_select
        if ready[0] == []:  # Timeout
            return
        time_received = time.time()
        rec_packet, addr = my_socket.recvfrom(1024)
        icmp_header = rec_packet[20:28]
        type, code, checksum, p_id, sequence = struct.unpack(
            'bbHHh', icmp_header)
        if p_id == packet_id:
            return time_received - time_sent
        time_left -= time_received - time_sent
        if time_left <= 0:
            return

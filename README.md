# Restless

Restless is a small in-memory implant using C#. It uses SharpPcap, which uses Npcap APIs internally. Npcap is a new standard library update to the old WinPcap library.  

Restless is a C2 that controls implants using ICMP-like packets. Restless implant listens for specific ICMP-like packets and applies instructions given by Restless-CLI.py. Restless Controller/Server can task clients to execute pre-baked or arbitrary commands.

### Status
- Has been successfully used on Windows7/10/12/16/19 and evaded detections on 10 :).
- Restless implants bypass Windows Inbound firewall rules.
- Server has a fully working CLI.
- Server sends encrypted messages, Caesar Cipher; it can be adjusted using the SHIFT parameter.
- Server uses raw sockets to send customized ICMP-like packets as described below.
- Server supports Command 2 All bots. 
- Client can execute arbitrary commands.
- Client can be shared by all team members (No need for team server).
- Restless’s Beacon payload is 19.0 KB without modifications.
- Integrated with [pwnboard](https://github.com/micahjmartin/pwnboard). 

### Dependencies:
- .NET Core


# Restless

### DISCLAIMERS
The information contained in this repo is for educational purposes ONLY! I DO NOT hold any responsibility for any misuse or damage of the information provided in my blog posts, discussions, activities, repositories, or exercises.

#### This is a low hanging fruit for Red-Blue themed competitions.

### What is Restless?
Restless is a small in-memory implant using C#. It uses SharpPcap, which uses Npcap APIs internally. Npcap is a new standard library update to the old WinPcap library.  

RestlessCLI is a C2 that controls Restless implants using ICMP-like packets. Restless implant listens for specific ICMP-like packets and applies instructions given by Restless-CLI.py. Restless Controller/Server can task clients to execute pre-baked or arbitrary commands.

![alt text](/poc.gif)


### Status
- Restless implants have been tested on Windows7/10/12/16/19 and evaded detections on 10 :).
- Restless implants bypass Windows Inbound firewall rules.
- Server CLI.
- Server sends encrypted messages, Caesar Cipher; it can be adjusted using the SHIFT parameter.
- Server uses raw sockets to send customized ICMP-like packets.
- Server supports Command 2 All bots. 
- All clients can be shared by all the red team members (No need for team server).
- The final payload is 20.0 KB without modifications.
- Integrated with pwnboard. 

### Files:
- Config.py Where are the configuration parameters. (Have to be changed according to your system)
- pwnAgent.py is a stand-alone script that updates pwnboard.
- ips.conf Where all the targeted IPs should be placed.

### Dependencies:
- Dotnet core
- Npcap

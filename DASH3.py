# derived from FamiLAB
# To God be all the glory! <3
import logging # for the following line
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # suppress IPV6 warning on startup
from scapy.all import * # for sniffing for the ARP packets
import requests # for posting to the IFTTT Maker Channel using HTTP POST
import time
import code
import os, sys
 
print('Initialization Done!')
print('Proceeding...')
print('RaspiPi Dash Sniffer')
print('Alpha v2 (c) 2017 RASPI TECHNOLOGIES')

lasttime = {}
buttons = { 'goldfish': '68:37:e9:c4:94:01',
            'ziploc': 'aa:bb:cc:dd:ee:ff'}

def arp_display(pkt):
    wa_login = '15555552121'
    wa_password = '[somepassword]'
    wa_dest = '15555551212'
    wa_msg = '"Button was pressed!"'
    cmd = 'yowsup-cli demos -l '+wa_login+':'+wa_password+' -s '+wa_dest+' '+wa_msg
    if not pkt.haslayer(Ether):
        return
    print pkt[Ether].src, pkt.summary()

    # ignore additional packets received within min_interval seconds
    mac = pkt[Ether].src
    min_interval = 5    # seconds
    global lasttime
    if not (mac in lasttime):
        interval = min_interval + 1     # we haven't see this; generate a fire
    else:
        interval = time.time() - lasttime[mac]

    if interval >= min_interval:
        lasttime[mac] = time.time()
        if mac == buttons['goldfish']:
            # post to IFTTT
            requests.post("https://maker.ifttt.com/trigger/Dash/with/key/_67EsfOnVbk8_twJUS-fU")
        elif mac == buttons['ziploc']:
            # send a WhatsApp message
            subprocess.Popen(cmd, shell=True)
        else:
            print 'We got a stray packet from an unknown device. Probably just Skynet.'

f = " or ".join(["ether host " + buttons[button] for button in buttons])
print f
print(sniff(iface="wlan0", prn=arp_display, filter=f, store=0))

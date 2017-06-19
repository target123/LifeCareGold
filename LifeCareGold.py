from gpiozero import MotionSensor
import RPi.GPIO as GPIO
import time, os
from subprocess import call
PIN = 27   #LED PIN
BPIN = 18  #Buzzer and RED LED PIN
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN,GPIO.OUT)  #LED Lights INIT
GPIO.output(PIN,GPIO.LOW) #LED Lights OUTPUT 
GPIO.setup(BPIN,GPIO.OUT) #Buzzer INIT
GPIO.output(BPIN,GPIO.LOW)#Buzzer OUTPUT
pir = MotionSensor(17)

#DASH Import Initializations

import logging # for the following line
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # suppress IPV6 warning on startup
from scapy.all import * # for sniffing for the ARP packets
import requests # for posting to the IFTTT Maker Channel using HTTP POST
import code
import sys
from interruptingcow import timeout   #Import LOOP ENDER

print('Initialization Done!')
print("\n\n")
print("-----------------------------------------------------------------------------")
print('Raspi-Pi ~ LifeCare Gold\n')
print('\nRelease Candidate v3.14 (c) 2017 RASPI TECHNOLOGIES INC.')
print("-----------------------------------------------------------------------------")
print("\n\n")
print("  _       _    __           ____                            ____           _       _ ")
print(" | |     (_)  / _|   ___   / ___|   __ _   _ __    ___     / ___|   ___   | |   __| |")
print(" | |     | | | |_   / _ \ | |      / _` | | '__|  / _ \   | |  _   / _ \  | |  / _` |")
print(" | |___  | | |  _| |  __/ | |___  | (_| | | |    |  __/   | |_| | | (_) | | | | (_| |")
print(" |_____| |_| |_|    \___|  \____|  \__,_| |_|     \___|    \____|  \___/  |_|  \__,_|")
print("")
print("        __,--'''''--,_        _,aad888baa,_")
print("     _-'              `\    ,d88888888888888b,_")
print("   ,'                   `\,d8888888888888888888b,")
print("  /                       `Y888888888888888888888b")
print(" /                `\        `Y88888888888888888888b")
print("(                  ,d,        `Y8888888888888888888b")
print("(                ,d888b,        `Y888888888888888888")
print("(              ,d8888888b,       I88888888888888888P")
print(" \           ,d88888888888ba,__,a88888888888888888P")
print("  \        ,d888888888888888888888888888888888888P")
print("   `.    ,d888888888888888888888888P'   `Y88888P'")
print("     \ ,d8888888P'd8888888888888P""(      `Y88""")
print("     ,d8888888P'd8888888888888P'    \       '<")
print("    d8888888P'd888888P'd888P""(      `\       )")
print("    Y88888P'd888888P'd888P'    \       `\    ,'")
print("     `""''d888888P'd88P""(      `\       `\-'")
print("         Y88888P'd88P'    \       `\      )")
print("          `"""'d8888(      `\       `\_,-'"")
print("              Y88888Pb,      `\      )""")
print("               `"""'d88b,      `\_,-'   "")
print("                  Y88888\      )       Dan")
print("                   `"""' `\_,-'"")
print("")
print('DEBUG: Remember to launch with sudo python from terminal! :)')

#Unitilized Espeak Modules
#cmd_beg= 'espeak -s120 -g5 -ven+f3 '
#cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null
#cmd= 'hi_Are_you_okay?___Please_press_the_DASH_button_to_confirm.'

def buzzer(): #Buuzer Function
    cycle_count = 0
    while (cycle_count != 6) :
        GPIO.output(BPIN, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(BPIN, GPIO.LOW)
        time.sleep(0.3)
        cycle_count = cycle_count + 1

#DASH Function Initializations

global triggered
triggered = 0 #Variable Hand-over

lasttime = {}
buttons = { 'goldfish': '68:37:e9:c4:94:01',
            'ziploc': 'aa:bb:cc:dd:ee:ff'}

def arp_display(pkt):
    wa_login = '15555552121'   #WhatsApp API Unutilized code
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
            global triggered #Setting triggered GLOBALLY as a variables
            triggered = 1            
            print("DASH BUTTON PRESSED!!!")
            print("Trigger value is: ", triggered)
            #requests.post("https://maker.ifttt.com/trigger/Dash/with/key/_67EsfOnVbk8_twJUS-fU")
        elif mac == buttons['ziploc']:
            # send a WhatsApp message
            subprocess.Popen(cmd, shell=True)
        else:
            print 'We got a stray packet from an unknown device. Probably just Skynet.'

print 'Ready'

f = " or ".join(["ether host " + buttons[button] for button in buttons])
print f

def dash():
    try:
        with timeout(15, exception=RuntimeError):
            print(sniff(iface="wlan0", prn=arp_display, filter=f, store=0))
    except RuntimeError:
        pass

while True:
    pir.wait_for_motion()
    GPIO.output(PIN,GPIO.HIGH)
    print("\n\n")
    print("Movement Detected! Lights ON!")
    pir.wait_for_no_motion()
    print("\n\n")
    print("NO Movement Detected! Lights OUT!")
    print("\n")
    #time.sleep(1)
    GPIO.output(PIN,GPIO.LOW)
    #call([cmd_beg+cmd+cmd_end], shell=True) #Readout Aloud by eSpeak
    buzzer()
    #print(sniff(iface="wlan0", prn=arp_display, filter=f, store=0))
    os.system('mpg123 -q /home/pi/Desktop/Alert.mp3 &') #Play MP3 Audio Prompt
    print("\nNOTIF: ~ Please press the DASH button within '15' seconds. ~")
    print("\nAwaiting DASH Button response...")
    buzzer()
    dash()
    #time.sleep(1)
    if triggered  != 0 :   #Check if DASH Button is pressed
        os.system('mpg123 -q /home/pi/Desktop/Confirm.mp3 &') #Play MP3 Confirm Prompt
        requests.post("https://maker.ifttt.com/trigger/Dash/with/key/_67EsfOnVbk8_twJUS-fU")
        triggered = 0      #Reset Variable for the next loop
    else:
        os.system('mpg123 -q /home/pi/Desktop/NotFound.mp3 &') #Play MP3 Not Received
        print("\nNOTIFICATION ALERT: The Dash Button was not detected during the time frame. Sending notifications to assigned contacts now.\n")

    #os.system('/home/pi/wiringPi/rpi-examples/buzzer/c/starwars &') #StarWars Buzzer Tester (Easter Egg)

print(sniff(iface="wlan0", prn=arp_display, filter=f, store=0))




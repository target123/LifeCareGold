from gpiozero import MotionSensor
import RPi.GPIO as GPIO
import time, os
from subprocess import call
PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN,GPIO.OUT)
GPIO.output(PIN,GPIO.LOW)
pir = MotionSensor(17)
STATUS = 0

cmd_beg= 'espeak -s120 -g5 -ven+f3 '
cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null
cmd= 'hi_Are_you_okay?___Please_press_the_DASH_button_to_confirm.'

print 'Ready'
while True:
    pir.wait_for_motion()
    GPIO.output(PIN,GPIO.HIGH)
    print("Movement Detected! Lights ON!")
    pir.wait_for_no_motion()
    print("NO Movement Detected! Lights OUT! Executing...")
    time.sleep(1)
    GPIO.output(PIN,GPIO.LOW)
    #call([cmd_beg+cmd+cmd_end], shell=True) #Readout Aloud by eSpeak
    os.system('mpg123 -q /home/pi/Desktop/Alert.mp3 &') #Play MP3 Audio Prompt
    time.sleep(1)
    #os.system('/home/pi/wiringPi/rpi-examples/buzzer/c/starwars &') 


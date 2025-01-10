# pip install RPi.GPIO simple_pid
# python -m pip install simple-pid

import RPi.GPIO as GPIO
from simple_pid import PID
import threading

# inicjacja pinów
GPIO.setmode(GPIO.BCM)

pwm_lewy_przod = 18 # pin 12
pwm_lewy = 13 # pin 33


import RPi.GPIO as GPIO
import socket
import time
import threading
from simple_pid import PID

licznik_R = 0
licznik_L = 0

adres_IP = '192.168.0.82'
port = 12345
data=None

#IBT2 silnik R
PWM_R_PIN = 13 #PIN  33
DIR_1_R_PIN = 6 #PIN 31
DIR_2_R_PIN = 26 #PIN 37

#IBT2 silnik L
PWM_L_PIN = 18 #PIN 12
DIR_1_L_PIN = 22 #PIN 15
DIR_2_L_PIN = 23 #PIN 16

#ENK R
ENC_R_PIN = 20 #PIN 38

#ENK L
ENC_L_PIN =16 #PIN 36


GPIO.setmode(GPIO.BCM)
#IBT2 silnik R
GPIO.setup(PWM_R_PIN, GPIO.OUT)
GPIO.setup(DIR_1_R_PIN, GPIO.OUT)
GPIO.setup(DIR_2_R_PIN, GPIO.OUT)
#IBT2 silnik L
GPIO.setup(PWM_L_PIN, GPIO.OUT)
GPIO.setup(DIR_1_L_PIN, GPIO.OUT)
GPIO.setup(DIR_2_L_PIN, GPIO.OUT)
#ENK R
GPIO.setup(ENC_R_PIN, GPIO.IN)
#ENK L
GPIO.setup(ENC_L_PIN, GPIO.IN)

#PWM
pwm_R = GPIO.PWM(PWM_R_PIN, 100)
pwm_L = GPIO.PWM(PWM_L_PIN, 100)
pwm_R.start(0)
pwm_L.start(0)

def hamulec():

    print("hamulec")
    pwm_R.stop()
    GPIO.output(DIR_1_R_PIN, False)
    GPIO.output(DIR_2_R_PIN, False)
    pwm_L.stop()
    GPIO.output(DIR_1_L_PIN, False)
    GPIO.output(DIR_2_L_PIN, False)
    global licznik_R
    global licznik_L
    licznik_R =0
    licznik_L =0

def ruch_przod():
    print("przod")

    GPIO.output(DIR_1_R_PIN, False)
    GPIO.output(DIR_2_R_PIN, True)

    GPIO.output(DIR_2_L_PIN, False)
    GPIO.output(DIR_1_L_PIN, True)
    global licznik_R
    global licznik_L
    licznik_R =0
    licznik_L =0


def ruch_tyl():
    print("tyl")
    GPIO.output(DIR_2_R_PIN, False)
    GPIO.output(DIR_1_R_PIN, True)

    GPIO.output(DIR_1_L_PIN, False)
    GPIO.output(DIR_2_L_PIN, True)
    global licznik_R
    global licznik_L
    licznik_R =0
    licznik_L =0

def ruch_lewo():
    print("lewo")
    GPIO.output(DIR_1_R_PIN, False)
    GPIO.output(DIR_2_R_PIN, True)
    global licznik_R
    global licznik_L
    licznik_R =0
    licznik_L =0

    GPIO.output(DIR_1_L_PIN, False)
    GPIO.output(DIR_2_L_PIN, True)

def ruch_prawo():
    print("prawo")
    GPIO.output(DIR_2_R_PIN, False)
    GPIO.output(DIR_1_R_PIN, True)

    GPIO.output(DIR_2_L_PIN, False)
    GPIO.output(DIR_1_L_PIN, True)
    global licznik_R
    global licznik_L
    licznik_R =0
    licznik_L =0

def start_server():
    GPIO.setmode(GPIO.BCM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((adres_IP, port))
        s.listen()
        print("Oczekiwanie na połączenie...")
        conn, addr = s.accept()

        with conn:
            print("Połączono z:", addr)
            pid_thread.start()
            odczyt_enkoderow.start()
            while True:
                data = conn.recv(1024)
                if not data:
                    hamulec()
                    break

                if data == b'przod':
                    ruch_przod()
                elif data == b'tyl':
                    ruch_tyl()
                elif data == b'lewo':
                    ruch_lewo()
                elif data == b'prawo':
                    ruch_prawo()
                elif data == b'hamulec':
                    hamulec()
                elif data == b'koniec':
                    pwm_R.stop()
                    pwm_L.stop()
                    hamulec()
                    GPIO.cleanup()
                    pid_thread.exit()
                    enc_read.exit()

                    exit()  
                    break

                print("Odebrano:", data)

def enc_read():
    GPIO.add_event_detect(ENC_R_PIN, GPIO.RISING, callback=lambda: enc_R)
    GPIO.add_event_detect(ENC_L_PIN, GPIO.RISING, callback=lambda: enc_L)

def enc_R():
    global licznik_R
    licznik_R += 1

def enc_L():
    global licznik_L
    licznik_L += 1

def pid():
    pid_R = PID(0.5, 0.1, 0.05, setpoint=0)
    pid_L = PID(0.5, 0.1, 0.05, setpoint=0)

    while True:
        pwm_R.start(pid_R(licznik_R))
        pwm_L.start(pid_L(licznik_L))
        time.sleep(0.3)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    hamulec()


    server_thread = threading.Thread(target=start_server)
    odczyt_enkoderow = threading.Thread(target=enc_read)
    pid_thread = threading.Thread(target=pid)
    server_thread.start()

    exit()

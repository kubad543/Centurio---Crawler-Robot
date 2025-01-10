import RPi.GPIO as GPIO
from time import sleep
import socket

ip_server = '192.168.0.82' # IP usatwione na stałe w routerze
port = 12345

GPIO.setmode(GPIO.BOARD)
silnik_lewy_przod = 36 # przod oznacza obrot zgodnie ze wskazowkami zegara
silnik_lewy_tyl = 38 # tyl oznacza obrot przeciwnie do wskazowek zegara
silnik_prawy_przod = 29
silnik_prawy_tyl = 7

GPIO.setup(silnik_lewy_przod, GPIO.OUT)
GPIO.setup(silnik_lewy_tyl, GPIO.OUT)
GPIO.setup(silnik_prawy_przod, GPIO.OUT)
GPIO.setup(silnik_prawy_tyl, GPIO.OUT)

def hamulec():
    print("hamulec")
    GPIO.output(silnik_lewy_przod, False)
    GPIO.output(silnik_lewy_tyl, False)
    GPIO.output(silnik_prawy_przod, False)
    GPIO.output(silnik_prawy_tyl, False)

def ruch_przod():
    print("przod")
    GPIO.output(silnik_prawy_tyl, False)
    GPIO.output(silnik_lewy_przod, False)
    GPIO.output(silnik_lewy_tyl, True)
    GPIO.output(silnik_prawy_przod, True)

def ruch_tyl():
    print("tyl")
    GPIO.output(silnik_lewy_tyl, False)
    GPIO.output(silnik_prawy_przod, False)
    GPIO.output(silnik_lewy_przod, True)
    GPIO.output(silnik_prawy_tyl, True)

def ruch_lewo():
    print("lewo")
    GPIO.output(silnik_lewy_tyl, False)
    GPIO.output(silnik_prawy_tyl, False)
    GPIO.output(silnik_lewy_przod, True)
    GPIO.output(silnik_prawy_przod, True)

def ruch_prawo():
    print("prawo")
    GPIO.output(silnik_lewy_przod, False)
    GPIO.output(silnik_prawy_przod, False)
    GPIO.output(silnik_lewy_tyl, True)
    GPIO.output(silnik_prawy_tyl, True)

def ruch_koniec():
    print("koniec")
    hamulec()
    GPIO.cleanup()
    exit()

def server():
    print("start")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_server, port))
    s.listen(1)
    #oczekliwanie na polaczenie komputera:
    conn, addr = s.accept()
    print("Connected by", addr)
    #inicjacja zegara odliczajacego sekundy
    zegar = 0
    #nasłuchiwanie komend
    while True:
        data = conn.recv(1024)
        if not data:
            hamulec()
            print('not data')
            break

        data = data.decode('utf-8')

        if zegar == 50:
            data = 'hamulec'
            zegar = 0

        print(data)
        if data == 'przod':
            zegar = 0
            ruch_przod()
        elif data == 'tyl':
            zegar = 0
            ruch_tyl()
        elif data == 'lewo':
            zegar = 0
            ruch_lewo()
        elif data == 'prawo':
            zegar = 0
            ruch_prawo()
        elif data == 'hamulec':
            hamulec()
        elif data == 'koniec':
            ruch_koniec()

if __name__ == "__main__":
    hamulec()
    server()

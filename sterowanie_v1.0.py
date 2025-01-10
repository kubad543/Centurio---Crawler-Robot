# sudo pip3 install pygame
#  haslo to centurio
import RPi.GPIO as GPIO #obsługa złącza GPIO
from time import sleep #biblioteka do obsługi opóźnień
import pygame

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

pygame.init()
win = pygame.display.set_mode((50,50))
print("start")
hamulec()
ostatni_ruch = "hamulec"
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if ostatni_ruch != "przod":
                    hamulec()
                    ostatni_ruch = "przod"
                    ruch_przod()
            elif event.key == pygame.K_DOWN:
                if ostatni_ruch != "tyl":
                    hamulec()
                    ostatni_ruch = "tyl"
                    ruch_tyl()
            elif event.key == pygame.K_LEFT:
                if ostatni_ruch != "lewo":
                    hamulec()
                    ostatni_ruch = "lewo"
                    ruch_lewo()
            elif event.key == pygame.K_RIGHT:
                if ostatni_ruch != "prawo":
                    hamulec()
                    ostatni_ruch = "prawo"
                    ruch_prawo()
            elif event.key == pygame.K_SPACE:
                if ostatni_ruch != "hamulec":
                    ostatni_ruch = "hamulec"
                    hamulec()
            elif event.key == pygame.K_ESCAPE:
                ruch_koniec()

    sleep(0.1)  # Adjust the sleep time if needed

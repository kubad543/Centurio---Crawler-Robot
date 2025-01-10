# nie dawać 5V na wejście GPIO, bo spalimy RPI
# 3,3V jest liczone jako logiczne 1, a 0V jako 0
#zapoznać się ze schematem wyprowadzeń pinów w RPI GPIO
import RPi.GPIO as GPIO #obsługa złącza GPIO
from time import sleep #biblioteka do obsługi opóźnień
GPIO.setmode(GPIO.BOARD)
inPin=40
GPIO.setup(inPin, GPIO.IN) # ustawienie pinu 40 jako wejściowy
try:
    while True:
        readVal = GPIO.input(inPin) # odczytanie wartości z pinu 40
        print(readVal) 
        sleep(1) # opóźnienie o 1 sekundę
except KeyboardInterrupt: #pętla się wykonuje w kółka aż nie naciśniemy jakiegoś przycisku. NIe mozna poprostu ctr+C, bo byśmy nie weszli do GPIO.cleanup()
    GPIO.cleanup()

import os
import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt
import threading
import socket
import keyboard

# Wczytaj model YOLOv5l6
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5l6.pt')


# Funkcja do rysowania wyników na obrazie
def draw_results(img, results):
    for *xyxy, conf, cls in results:
        label = f'{model.names[int(cls)]} {conf:.2f}'
        plot_one_box(xyxy, img, label=label)


def plot_one_box(xyxy, img, label=None, color=(0, 255, 0), line_thickness=3):
    # Rysowanie prostokąta na obrazie
    tl = line_thickness or round(0.002 * max(img.shape[0:2])) + 1
    c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
    bounding_box_center = [(c1[0]+c2[0])/2,(c1[1]+c2[1])/2 ]
    # print(bounding_box_center)
    # Rysuj kropkę w środku bounding boxa
    cv2.circle(img, (int(bounding_box_center[0]), int(bounding_box_center[1])), 3, color, -1)
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

def detect_bottles(frame):
    results = model(frame)  # Wykryj obiekty

    # Przetwórz wyniki
    bottles = []
    for result in results.xyxy[0]:  # Przetwórz wyniki detekcji
        if model.names[int(result[5])] == 'bottle':  # Sprawdź, czy wykryty obiekt to butelka
            bottles.append(result)

    # Rysuj wyniki na obrazie, jeśli wykryto butelki
    if bottles:
        draw_results(frame, bottles)
        return True, frame
    return False, frame
#Czy udało się otworzyć strumień



def operate_on_image():

    ip_address = '192.168.0.82'
    cap = cv2.VideoCapture(f"http://{ip_address}:12344/video_feed")

    while True:
        ret, frame = cap.read()

        if not cap.isOpened():
            print("Failed to open camera")
            exit()

        if not ret:
            print("Failed to read frame from camera")
            break

        # Operacje na klatce
        has_bottle, processed_frame = detect_bottles(frame)

        # Wyświetl obraz z zaznaczoną butelką
        cv2.imshow("Detekcja butelek", processed_frame)

        # Przerwanie pętli po naciśnięciu klawisza 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    exit()

def server():
   
    s.connect((ip, port))
    camera_thread.start()
    keyboard.on_press(on_key_event)
    keyboard.wait('esc')
    s.close()
    camera_thread.join()
    control_thread.join()


def send_data(data):
    s.send(data.encode('utf-8'))

def on_key_event(event):
    # print("wciśnięto: " + event.name)
    if event.name == 'w':
        send_data('przod')
    elif event.name == 's':
        send_data('tyl')
    elif event.name == 'a':
        send_data('lewo')
    elif event.name == 'd':
        send_data('prawo')
    elif event.name == 'space':
        send_data('hamulec')
    elif event.name == 'esc':
        send_data('koniec')
        s.close()
        cv2.destroyAllWindows()
        exit()


if __name__=="__main__":

    camera_thread = threading.Thread(target = operate_on_image)
    control_thread = threading.Thread(target = server)

    print("start")

    ip = '192.168.0.82'
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_thread.start()

    control_thread.join()
    camera_thread.join()

    
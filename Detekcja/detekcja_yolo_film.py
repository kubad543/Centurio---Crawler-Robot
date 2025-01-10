import os
import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Wczytaj model YOLOv5l6
model = torch.hub.load('ultralytics/yolov5', 'custom', path='Detekcja/yolov5l6.pt')


ip_address = '192.168.0.82'
cap = cv2.VideoCapture(f"http://{ip_address}:12344/video_feed")

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

if not cap.isOpened():
    print("Failed to open camera")
    exit()


while True:
    ret, frame = cap.read()

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

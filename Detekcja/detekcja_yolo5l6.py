import os
import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt

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
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


# Funkcja do detekcji butelek na obrazie
def detect_bottles(image_path):
    img = cv2.imread(image_path)  # Wczytaj obraz
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return False, img

    results = model(img)  # Wykryj obiekty

    # Przetwórz wyniki
    bottles = []
    for result in results.xyxy[0]:  # Przetwórz wyniki detekcji
        if model.names[int(result[5])] == 'bottle':  # Sprawdź, czy wykryty obiekt to butelka
            bottles.append(result)

    # Rysuj wyniki na obrazie, jeśli wykryto butelki
    if bottles:
        draw_results(img, bottles)
        return True, img
    return False, img


# Przetwarzanie wszystkich obrazów w folderze input
input_folder = 'input'
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        has_bottle, processed_img = detect_bottles(input_path)
        if has_bottle:
            print(f'{filename}: tak')
            # Zapisz obraz z zaznaczoną butelką
            cv2.imwrite(output_path, processed_img)
        else:
            print(f'{filename}: nie')

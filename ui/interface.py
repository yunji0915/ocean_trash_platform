import tkinter as tk
from tkinter import LabelFrame
from PIL import Image, ImageTk
import cv2
from yolov8_detect import detect_objects, get_box_color
from drone_control import get_frame
from telegram_bot import send_image_with_location
import asyncio
import os
import datetime
import tkintermapview

current_frame = None
captured_image_label = None

def save_image(frame, label="drone_capture"):
    global captured_image_label
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Captured_Images")
    os.makedirs(desktop_path, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(desktop_path, f"capture_{label}_{timestamp}.png")
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image.save(file_path)
    asyncio.run(send_image_with_location(file_path, 'images/map.png'))
    preview = ImageTk.PhotoImage(image.resize((400, 300)))
    captured_image_label.config(image=preview)
    captured_image_label.image = preview

def capture_image():
    global current_frame
    if current_frame is not None:
        save_image(current_frame)

def video_stream():
    global current_frame
    frame = get_frame()
    current_frame = frame.copy()

    results = detect_objects(frame)
    detected = []

    for result in results:
        for box in result.boxes:
            if box.conf.item() > 0.65:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls.item())
                class_name = result.names[class_id]
                confidence = box.conf.item()
                label = f"{class_name} {confidence:.2f}"
                detected.append((class_name, confidence))
                color = get_box_color(class_name)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    if detected:
        names = ", ".join([d[0] for d in detected])
        count = len(detected)
        avg = sum(d[1] for d in detected) / count
        lines = [f"Objects: {names}", f"Count: {count}", f"Confidence: {avg:.2f}"]
        for i, line in enumerate(lines):
            cv2.putText(frame, line, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (800, 800))
    img = ImageTk.PhotoImage(Image.fromarray(resized))
    video_label.config(image=img)
    video_label.image = img
    window.after(10, video_stream)

def show_interface():
    global video_label, window, captured_image_label
    window = tk.Tk()
    window.title("AI Water Trash Detection Drone")
    window.geometry("1200x800")
    window.configure(bg="#D9D9D9")

    left_frame = tk.Frame(window, bg="#D9D9D9")
    left_frame.grid(row=0, column=0, padx=10, pady=10)

    video_label = tk.Label(left_frame, bg="#D9D9D9")
    video_label.pack()

    right_frame = tk.Frame(window, bg="#D9D9D9")
    right_frame.grid(row=0, column=1, padx=10, pady=10)

    captured_image_label = tk.Label(right_frame, bg="#D9D9D9")
    captured_image_label.pack()

    map_label = LabelFrame(right_frame, text="Map", padx=5, pady=5)
    map_label.pack()

    map_widget = tkintermapview.TkinterMapView(map_label, width=400, height=300, corner_radius=0)
    map_widget.set_position(35.157038, 129.163116)
    map_widget.set_zoom(15)
    map_widget.pack()

    button = tk.Button(window, text="📸 캡처", command=capture_image, font=("맑은 고딕", 16), bg="#AACCEE")
    button.grid(row=1, column=0, columnspan=2, pady=20)

    window.after(0, video_stream)
    window.mainloop()

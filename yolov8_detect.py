from ultralytics import YOLO

model = YOLO('models/best_final.pt')

def detect_objects(frame, conf=0.65):
    return model(frame, conf=conf)

def get_box_color(class_name):
    colors = {
        'Aluminum-can': (0, 255, 0),
        'Plastic-bottle': (255, 0, 0),
        'Buoy': (0, 0, 255)
    }
    return colors.get(class_name, (255, 255, 0))

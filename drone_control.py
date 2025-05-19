from djitellopy import Tello

tello = Tello()

def connect_drone():
    tello.connect()
    tello.streamon()

def get_frame():
    return tello.get_frame_read().frame

def execute_command(command):
    print(f"드론 명령 실행: {command}")

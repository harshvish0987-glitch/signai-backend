import math

def dist(a, b):
    return math.sqrt(
        (a["x"] - b["x"]) ** 2 +
        (a["y"] - b["y"]) ** 2 +
        ((a.get("z", 0) - b.get("z", 0)) ** 2)
    )

def is_finger_extended(landmarks, tip, pip):
    return landmarks[tip]["y"] < landmarks[pip]["y"] - 0.02

def is_thumb_extended(landmarks):
    tip = landmarks[4]
    ip = landmarks[3]
    wrist = landmarks[0]
    return abs(tip["x"] - wrist["x"]) > abs(ip["x"] - wrist["x"]) * 1.2

def predict_gesture(landmarks):
    thumb = is_thumb_extended(landmarks)
    index = is_finger_extended(landmarks, 8, 6)
    middle = is_finger_extended(landmarks, 12, 10)
    ring = is_finger_extended(landmarks, 16, 14)
    pinky = is_finger_extended(landmarks, 20, 18)

    extended = [thumb, index, middle, ring, pinky].count(True)

    if extended == 0:
        return "Stop", 0.90

    if index and not any([thumb, middle, ring, pinky]):
        return "Point", 0.92

    if thumb and not any([index, middle, ring, pinky]):
        return "Good", 0.91

    if thumb and index and pinky and not middle and not ring:
        return "I Love You", 0.95

    if extended == 5:
        return "Hello", 0.93

    return None, 0.0

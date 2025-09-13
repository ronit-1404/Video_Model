"""
Student Attention Detection - Video Script (Refactored)

This script detects student attention and emotion from a video or webcam using OpenCV and a Keras model.
"""
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import imutils
import os

# Paths (relative to project root)
HAAR_FACE = os.path.join('..', 'haarcascades', 'haarcascade_frontalface_default.xml')
HAAR_EYE = os.path.join('..', 'haarcascades', 'haarcascade_eye.xml')
MODEL_PATH = os.path.join('..', 'models', 'model_num.hdf5')
SAMPLE_VIDEO = os.path.join('..', 'samples', 'live_vid2.mp4')

# Debug: Check if Haar cascade XML files exist
print("Face cascade path:", HAAR_FACE)
print("Exists?", os.path.exists(HAAR_FACE))
print("Eye cascade path:", HAAR_EYE)
print("Exists?", os.path.exists(HAAR_EYE))

# Load Haarcascades
face_cascade = cv2.CascadeClassifier(HAAR_FACE)
eye_cascade = cv2.CascadeClassifier(HAAR_EYE)

# Load emotion model
emotion_classifier = load_model(MODEL_PATH, compile=False)
EMOTIONS = ["angry", "disgust", "fear", "happy", "sad", "surprised", "neutral"]

# Map model emotions to 4 target emotions
EMOTION_MAP = {
    "angry": "frustrated",
    "disgust": "frustrated",
    "fear": "confused",
    "happy": "focused",
    "sad": "bored",
    "surprised": "focused",
    "neutral": "focused"
}
TARGET_EMOTIONS = ["bored", "confused", "frustrated", "focused"]

# Video source: set to 0 for webcam, or use SAMPLE_VIDEO for file
USE_LIVE_VIDEO = True
VIDEO_SOURCE = 0 if USE_LIVE_VIDEO else SAMPLE_VIDEO

cv2.namedWindow('Student Attention Detector')

while True:
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        break
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        canvas = np.zeros((350, 400, 3), dtype="uint8")
        if len(faces) == 0:
            cv2.putText(frame, "Not-Attentive (student unavailable)", (10, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi)
            for (ex, ey, ew, eh) in eyes[:2]:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            roi_resized = cv2.resize(roi, (48, 48))
            roi_resized = roi_resized.astype("float") / 255.0
            roi_resized = img_to_array(roi_resized)
            roi_resized = np.expand_dims(roi_resized, axis=0)
            preds = emotion_classifier.predict(roi_resized)[0]
            # Map probabilities to 4 target emotions
            mapped_probs = {e: 0.0 for e in TARGET_EMOTIONS}
            for i, prob in enumerate(preds):
                mapped_emotion = EMOTION_MAP[EMOTIONS[i]]
                mapped_probs[mapped_emotion] += prob
            # Get the max mapped emotion
            label = max(mapped_probs, key=mapped_probs.get)
            attentive = len(eyes) >= 1
            label_text = f"{'Attentive' if attentive else 'Not-Attentive'} ({label})"
            cv2.putText(frame, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            # Show mapped probabilities
            for i, emotion in enumerate(TARGET_EMOTIONS):
                prob = mapped_probs[emotion]
                text = f"{emotion}: {prob * 100:.2f}%"
                w_bar = int(prob * 300)
                cv2.rectangle(canvas, (7, (i * 35) + 5), (w_bar, (i * 35) + 35), (0, 0, 255), -1)
                cv2.putText(canvas, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
        cv2.imshow('Student Attention Detector', frame)
        cv2.imshow('Face Emotion Probabilities using AI', canvas)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    break

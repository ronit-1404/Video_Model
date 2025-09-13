import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import librosa
import os

class EmotionDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
        self.audio_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
        
        # Load models
        self.load_models()
    
    def load_models(self):
        try:
            self.emotion_model = load_model('models/model_num.hdf5')
            print("Video emotion model loaded successfully")
        except Exception as e:
            print(f"Error loading video emotion model: {e}")
            self.emotion_model = None
        
        try:
            self.audio_model = load_model('models/audio_model7label_CNN.hdf5')
            print("Audio emotion model loaded successfully")
        except Exception as e:
            print(f"Error loading audio emotion model: {e}")
            self.audio_model = None
    
    def detect_emotions(self, frame):
        if self.emotion_model is None:
            return []
        
        emotions = []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for i, (x, y, w, h) in enumerate(faces):
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            roi_gray = roi_gray.astype('float32') / 255.0
            roi_gray = np.expand_dims(roi_gray, axis=0)
            roi_gray = np.expand_dims(roi_gray, axis=-1)
            
            try:
                predictions = self.emotion_model.predict(roi_gray, verbose=0)
                emotion_idx = np.argmax(predictions[0])
                confidence = np.max(predictions[0])
                
                emotion_data = {
                    'person_id': i,
                    'bbox': (x, y, w, h),
                    'dominant_emotion': self.emotion_labels[emotion_idx],
                    'confidence': float(confidence),
                    'all_emotions': {
                        label: float(prob) for label, prob in zip(self.emotion_labels, predictions[0])
                    }
                }
                emotions.append(emotion_data)
            except Exception as e:
                print(f"Error predicting emotion: {e}")
        
        return emotions
    
    def detect_audio_emotions(self, audio_path):
        if self.audio_model is None:
            return None
        
        try:
            # Load and preprocess audio
            audio, sr = librosa.load(audio_path, sr=22050, duration=30)
            
            # Extract features (MFCC)
            mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
            mfccs = np.mean(mfccs.T, axis=0)
            mfccs = np.expand_dims(mfccs, axis=0)
            mfccs = np.expand_dims(mfccs, axis=-1)
            
            # Predict emotions
            predictions = self.audio_model.predict(mfccs, verbose=0)
            
            emotion_probs = {
                label: float(prob) for label, prob in zip(self.audio_labels, predictions[0])
            }
            
            return emotion_probs
            
        except Exception as e:
            print(f"Error in audio emotion detection: {e}")
            return None
    
    def get_emotion_color(self, emotion):
        color_map = {
            'Happy': (0, 255, 0),      # Green
            'Sad': (255, 0, 0),        # Blue
            'Angry': (0, 0, 255),      # Red
            'Fear': (128, 0, 128),     # Purple
            'Surprise': (255, 255, 0), # Cyan
            'Disgust': (0, 128, 0),    # Dark Green
            'Neutral': (128, 128, 128) # Gray
        }
        return color_map.get(emotion, (255, 255, 255))
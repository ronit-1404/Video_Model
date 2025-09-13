import cv2
import numpy as np

class VideoProcessor:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.thickness = 2
    
    def draw_emotions(self, frame, emotions, options):
        """Draw emotion labels and bounding boxes on frame"""
        processed_frame = frame.copy()
        
        for emotion_data in emotions:
            x, y, w, h = emotion_data['bbox']
            emotion = emotion_data['dominant_emotion']
            confidence = emotion_data['confidence']
            
            # Get color for emotion
            from utils.emotion_detector import EmotionDetector
            detector = EmotionDetector()
            color = detector.get_emotion_color(emotion)
            
            # Draw bounding box
            cv2.rectangle(processed_frame, (x, y), (x+w, y+h), color, 2)
            
            # Prepare label text
            label_parts = []
            if options.get('show_emotions', True):
                label_parts.append(emotion)
            if options.get('show_confidence', True):
                label_parts.append(f"{confidence:.2f}")
            
            label = " | ".join(label_parts)
            
            # Draw label background
            label_size = cv2.getTextSize(label, self.font, self.font_scale, self.thickness)[0]
            cv2.rectangle(
                processed_frame,
                (x, y - label_size[1] - 10),
                (x + label_size[0], y),
                color,
                -1
            )
            
            # Draw label text
            cv2.putText(
                processed_frame,
                label,
                (x, y - 5),
                self.font,
                self.font_scale,
                (255, 255, 255),
                self.thickness
            )
        
        return processed_frame
    
    def resize_frame(self, frame, max_width=640, max_height=480):
        """Resize frame while maintaining aspect ratio"""
        h, w = frame.shape[:2]
        
        # Calculate scaling factor
        scale_w = max_width / w
        scale_h = max_height / h
        scale = min(scale_w, scale_h, 1.0)  # Don't upscale
        
        if scale < 1.0:
            new_w = int(w * scale)
            new_h = int(h * scale)
            frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        return frame
    
    def apply_filters(self, frame, filter_type=None):
        """Apply visual filters to frame"""
        if filter_type == "grayscale":
            return cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        elif filter_type == "blur":
            return cv2.GaussianBlur(frame, (15, 15), 0)
        elif filter_type == "sharpen":
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            return cv2.filter2D(frame, -1, kernel)
        else:
            return frame
    
    def add_overlay_info(self, frame, info_text, position=(10, 30)):
        """Add overlay information to frame"""
        processed_frame = frame.copy()
        
        # Add semi-transparent background
        overlay = processed_frame.copy()
        cv2.rectangle(overlay, (0, 0), (400, 80), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, processed_frame, 0.3, 0, processed_frame)
        
        # Add text
        y_offset = position[1]
        for line in info_text.split('\n'):
            cv2.putText(
                processed_frame,
                line,
                (position[0], y_offset),
                self.font,
                0.6,
                (255, 255, 255),
                1
            )
            y_offset += 25
        
        return processed_frame
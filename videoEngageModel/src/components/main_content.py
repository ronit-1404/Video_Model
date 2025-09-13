import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import tempfile
import os

def render_main_content(options):
    if options["analysis_type"] == "Real-time Video":
        render_realtime_analysis(options)
    elif options["analysis_type"] == "Upload Video":
        render_upload_analysis(options)
    elif options["analysis_type"] == "Sample Videos":
        render_sample_analysis(options)
    elif options["analysis_type"] == "Audio Analysis":
        render_audio_analysis(options)

def render_realtime_analysis(options):
    st.subheader("📹 Real-time Video Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        start_button = st.button("Start Camera", type="primary")
        stop_button = st.button("Stop Camera")
        
        video_placeholder = st.empty()
    
    with col2:
        emotion_placeholder = st.empty()
        metrics_placeholder = st.empty()
    
    if start_button and not st.session_state.get('camera_running', False):
        st.session_state.camera_running = True
        st.session_state.emotion_data = []
        
        cap = cv2.VideoCapture(options["camera_source"])
        
        while st.session_state.get('camera_running', False):
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to access camera")
                break
            
            # Process frame for emotions
            emotions = st.session_state.emotion_detector.detect_emotions(frame)
            processed_frame = st.session_state.video_processor.draw_emotions(
                frame, emotions, options
            )
            
            # Display frame
            video_placeholder.image(processed_frame, channels="BGR", use_column_width=True)
            
            # Update emotion data
            if emotions:
                timestamp = datetime.now().strftime("%H:%M:%S")
                for emotion_data in emotions:
                    emotion_data['timestamp'] = timestamp
                    st.session_state.emotion_data.append(emotion_data)
                
                # Update emotion display
                with emotion_placeholder.container():
                    display_current_emotions(emotions)
                
                # Update metrics
                with metrics_placeholder.container():
                    display_emotion_metrics()
            
            if stop_button:
                st.session_state.camera_running = False
                break
        
        cap.release()
    
    if stop_button:
        st.session_state.camera_running = False

def render_upload_analysis(options):
    st.subheader("📁 Upload Video Analysis")
    
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=['mp4', 'avi', 'mov', 'mkv']
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name
        
        process_video_file(temp_path, options)
        
        # Clean up temp file
        os.unlink(temp_path)

def render_sample_analysis(options):
    st.subheader("🎬 Sample Video Analysis")
    
    if options["sample_video"]:
        sample_path = f"samples/{options['sample_video']}"
        
        if os.path.exists(sample_path):
            st.info(f"Analyzing: {options['sample_video']}")
            process_video_file(sample_path, options)
        else:
            st.error(f"Sample video not found: {sample_path}")

def render_audio_analysis(options):
    st.subheader("🔊 Audio Emotion Analysis")
    
    uploaded_audio = st.file_uploader(
        "Choose an audio file",
        type=['wav', 'mp3', 'ogg', 'm4a']
    )
    
    if uploaded_audio is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(uploaded_audio.read())
            temp_path = tmp_file.name
        
        # Process audio for emotions
        audio_emotions = st.session_state.emotion_detector.detect_audio_emotions(temp_path)
        
        if audio_emotions:
            display_audio_emotions(audio_emotions)
        
        os.unlink(temp_path)

def process_video_file(video_path, options):
    st.session_state.emotion_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    frame_count = 0
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        video_placeholder = st.empty()
    
    with col2:
        emotion_placeholder = st.empty()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process every nth frame to speed up analysis
        if frame_count % 5 == 0:
            emotions = st.session_state.emotion_detector.detect_emotions(frame)
            processed_frame = st.session_state.video_processor.draw_emotions(
                frame, emotions, options
            )
            
            video_placeholder.image(processed_frame, channels="BGR", use_column_width=True)
            
            if emotions:
                timestamp = frame_count / fps
                for emotion_data in emotions:
                    emotion_data['timestamp'] = timestamp
                    st.session_state.emotion_data.append(emotion_data)
                
                with emotion_placeholder.container():
                    display_current_emotions(emotions)
        
        frame_count += 1
        progress = frame_count / total_frames
        progress_bar.progress(progress)
        status_text.text(f"Processing frame {frame_count}/{total_frames}")
    
    cap.release()
    status_text.text("Analysis complete!")
    
    # Display final analytics
    if options["show_charts"] and st.session_state.emotion_data:
        display_emotion_analytics()

def display_current_emotions(emotions):
    st.write("**Current Emotions:**")
    for i, emotion in enumerate(emotions):
        st.write(f"Person {i+1}: {emotion.get('dominant_emotion', 'Unknown')} "
                f"({emotion.get('confidence', 0):.2f})")

def display_emotion_metrics():
    if not st.session_state.emotion_data:
        return
    
    df = pd.DataFrame(st.session_state.emotion_data)
    
    # Calculate metrics
    total_detections = len(df)
    unique_people = df['person_id'].nunique() if 'person_id' in df.columns else 1
    
    st.metric("Total Detections", total_detections)
    st.metric("People Detected", unique_people)
    
    if 'dominant_emotion' in df.columns:
        most_common = df['dominant_emotion'].mode().iloc[0] if not df['dominant_emotion'].mode().empty else "None"
        st.metric("Most Common Emotion", most_common)

def display_emotion_analytics():
    if not st.session_state.emotion_data:
        return
    
    st.subheader("📊 Emotion Analytics")
    
    df = pd.DataFrame(st.session_state.emotion_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Emotion distribution pie chart
        if 'dominant_emotion' in df.columns:
            emotion_counts = df['dominant_emotion'].value_counts()
            fig = px.pie(
                values=emotion_counts.values,
                names=emotion_counts.index,
                title="Emotion Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Emotion timeline
        if 'timestamp' in df.columns and 'dominant_emotion' in df.columns:
            timeline_df = df.groupby(['timestamp', 'dominant_emotion']).size().reset_index(name='count')
            fig = px.line(
                timeline_df,
                x='timestamp',
                y='count',
                color='dominant_emotion',
                title="Emotion Timeline"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed data table
    if st.checkbox("Show Detailed Data"):
        st.dataframe(df)

def display_audio_emotions(audio_emotions):
    st.subheader("🎵 Audio Emotion Results")
    
    if isinstance(audio_emotions, dict):
        # Display emotion probabilities
        emotions_df = pd.DataFrame(list(audio_emotions.items()), columns=['Emotion', 'Confidence'])
        
        # Bar chart
        fig = px.bar(
            emotions_df,
            x='Emotion',
            y='Confidence',
            title="Audio Emotion Confidence Scores"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display top emotion
        top_emotion = max(audio_emotions, key=audio_emotions.get)
        st.success(f"Detected Emotion: **{top_emotion}** (Confidence: {audio_emotions[top_emotion]:.2f})")
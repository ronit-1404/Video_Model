import streamlit as st
import os

def render_sidebar():
    st.sidebar.title("🎯 Configuration")
    
    # Analysis type selection
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Real-time Video", "Upload Video", "Sample Videos", "Audio Analysis"]
    )
    
    # Model selection
    st.sidebar.subheader("Model Settings")
    emotion_model = st.sidebar.selectbox(
        "Emotion Detection Model",
        ["CNN Model", "Advanced Model"]
    )
    
    # Confidence threshold
    confidence_threshold = st.sidebar.slider(
        "Confidence Threshold",
        min_value=0.1,
        max_value=1.0,
        value=0.5,
        step=0.1
    )
    
    # Real-time settings
    if analysis_type == "Real-time Video":
        st.sidebar.subheader("Camera Settings")
        camera_source = st.sidebar.selectbox(
            "Camera Source",
            [0, 1, 2]  # Different camera indices
        )
        
        frame_rate = st.sidebar.slider(
            "Frame Rate",
            min_value=1,
            max_value=30,
            value=10
        )
    else:
        camera_source = None
        frame_rate = None
    
    # Sample video selection
    sample_video = None
    if analysis_type == "Sample Videos":
        sample_videos = [
            "emotions.mp4",
            "live_vid.mp4", 
            "live_vid2.mp4",
            "live_vid3.mp4",
            "stanford_lecture2.mp4",
            "videoplayback.mp4"
        ]
        sample_video = st.sidebar.selectbox(
            "Select Sample Video",
            sample_videos
        )
    
    # Display options
    st.sidebar.subheader("Display Options")
    show_emotions = st.sidebar.checkbox("Show Emotion Labels", value=True)
    show_confidence = st.sidebar.checkbox("Show Confidence Scores", value=True)
    show_charts = st.sidebar.checkbox("Show Analytics Charts", value=True)
    
    return {
        "analysis_type": analysis_type,
        "emotion_model": emotion_model,
        "confidence_threshold": confidence_threshold,
        "camera_source": camera_source,
        "frame_rate": frame_rate,
        "sample_video": sample_video,
        "show_emotions": show_emotions,
        "show_confidence": show_confidence,
        "show_charts": show_charts
    }
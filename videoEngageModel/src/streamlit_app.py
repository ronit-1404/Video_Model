import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.sidebar import render_sidebar

from components.main_content import render_main_content
from utils.emotion_detector import EmotionDetector
from utils.video_processor import VideoProcessor

st.set_page_config(
    page_title="Video Engagement Analytics",
    page_icon="!!",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .stAlert {
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)


def main():
    if 'emotion_detector' not in st.session_state:
        st.session_state.emotion_detector = EmotionDetector()

    if 'video_processor' not in st.session_state:
        st.session_state.video_processor = VideoProcessor()
    

    st.markdown("<h1 class='main-header'>🎭 Video Engagement Analytics</h1>", unsafe_allow_html=True)
    
    
    sidebar_options = render_sidebar()
    
    render_main_content(sidebar_options)

if __name__ == "__main__":
    main()
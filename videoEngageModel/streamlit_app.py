import streamlit as stimport streamlit as st

import sysimport sys

import osimport os



# Add the src directory to the Python path# Add the src directory to the Python path

src_path = os.path.join(os.path.dirname(__file__), 'src')src_path = os.path.join(os.path.dirname(__file__), 'src')

sys.path.insert(0, src_path)sys.path.insert(0, src_path)



# Test cv2 availability first# Test cv2 availability first

try:try:

    import cv2    import cv2

    cv2_available = True    cv2_available = True

    st.success(f"✅ OpenCV version {cv2.__version__} loaded successfully!")    st.success(f"✅ OpenCV version {cv2.__version__} loaded successfully!")

except ImportError as e:except ImportError as e:

    cv2_available = False    cv2_available = False

    st.error("❌ OpenCV (cv2) is not available!")    st.error("❌ OpenCV (cv2) is not available!")

    st.error(f"Import error details: {str(e)}")    st.error(f"Import error details: {str(e)}")

        

    # Additional debugging information    # Additional debugging information

    import sys, os    import sys, os

    st.write("**Debug Information:**")    st.write("**Debug Information:**")

    st.write(f"- Python version: {sys.version}")    st.write(f"- Python version: {sys.version}")

    st.write(f"- Current directory: {os.getcwd()}")    st.write(f"- Current directory: {os.getcwd()}")

    st.write(f"- Python path: {sys.path[:3]}...")  # Show first 3 entries    st.write(f"- Python path: {sys.path[:3]}...")  # Show first 3 entries

        

    # Check if files exist    # Check if files exist

    files_to_check = ["requirements.txt", "packages.txt"]    files_to_check = ["requirements.txt", "packages.txt"]

    for file in files_to_check:    for file in files_to_check:

        if os.path.exists(file):        if os.path.exists(file):

            st.write(f"- ✅ {file} exists")            st.write(f"- ✅ {file} exists")

        else:        else:

            st.write(f"- ❌ {file} missing")            st.write(f"- ❌ {file} missing")

        

    st.info("📝 Troubleshooting steps:")    st.info("📝 Troubleshooting steps:")

    st.markdown("""    st.markdown("""

    1. Make sure `requirements.txt` includes `opencv-python-headless==4.8.1.78`    1. Make sure `requirements.txt` includes `opencv-python-headless==4.8.1.78`

    2. Make sure `packages.txt` includes system dependencies      2. Make sure `packages.txt` includes system dependencies  

    3. Try **redeploying** your app on Streamlit Cloud (clear cache)    3. Try **redeploying** your app on Streamlit Cloud (clear cache)

    4. Check that all files are in your repository **root directory**    4. Check that all files are in your repository **root directory**

    5. Run the debug app: `debug_opencv.py` for detailed diagnostics    5. Run the debug app: `debug_opencv.py` for detailed diagnostics

    """)    """)

        

    st.warning("🔧 **For Streamlit Cloud**: Try clicking 'Reboot app' in the app menu to clear cache.")    st.warning("🔧 **For Streamlit Cloud**: Try clicking 'Reboot app' in the app menu to clear cache.")

    st.stop()    st.stop()



try:try:

    from components.sidebar import render_sidebar    from components.sidebar import render_sidebar

    from components.main_content import render_main_content    from components.main_content import render_main_content

    from utils.emotion_detector import EmotionDetector    from utils.emotion_detector import EmotionDetector

    from utils.video_processor import VideoProcessor    from utils.video_processor import VideoProcessor

except ImportError as e:except ImportError as e:

    st.error(f"Failed to import required modules: {e}")    st.error(f"Failed to import required modules: {e}")

    st.info("Please ensure all dependencies are installed properly.")    st.info("Please ensure all dependencies are installed properly.")

    st.stop()    st.stop()



st.set_page_config(st.set_page_config(

    page_title="Video Engagement Analytics",    page_title="Video Engagement Analytics",

    page_icon="🎭",    page_icon="🎭",

    layout="wide",    layout="wide",

    initial_sidebar_state="expanded"    initial_sidebar_state="expanded"

))



st.markdown("""st.markdown("""

<style><style>

    .main-header {    .main-header {

        text-align: center;        text-align: center;

        color: #1f77b4;        color: #1f77b4;

        margin-bottom: 30px;        margin-bottom: 30px;

    }    }

    .stAlert {    .stAlert {

        margin-top: 20px;        margin-top: 20px;

    }    }

</style></style>

""", unsafe_allow_html=True)""", unsafe_allow_html=True)



def main():def main():

    if 'emotion_detector' not in st.session_state:    if 'emotion_detector' not in st.session_state:

        st.session_state.emotion_detector = EmotionDetector()        st.session_state.emotion_detector = EmotionDetector()



    if 'video_processor' not in st.session_state:    if 'video_processor' not in st.session_state:

        st.session_state.video_processor = VideoProcessor()        st.session_state.video_processor = VideoProcessor()

        

    st.markdown("<h1 class='main-header'>🎭 Video Engagement Analytics</h1>", unsafe_allow_html=True)    st.markdown("<h1 class='main-header'>🎭 Video Engagement Analytics</h1>", unsafe_allow_html=True)

        

    sidebar_options = render_sidebar()    sidebar_options = render_sidebar()

        

    render_main_content(sidebar_options)    render_main_content(sidebar_options)



if __name__ == "__main__":if __name__ == "__main__":

    main()    main()
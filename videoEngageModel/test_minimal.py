import streamlit as st
import sys
import os

st.title("🧪 Minimal OpenCV Test")
st.write("Ultra-simple test to verify OpenCV works on Streamlit Cloud")

# Environment info
st.subheader("🔍 Environment")
st.write(f"**Python:** {sys.version}")
st.write(f"**Directory:** {os.getcwd()}")

# OpenCV test
st.subheader("🎯 OpenCV Test")
try:
    import cv2
    st.success(f"✅ SUCCESS! OpenCV {cv2.__version__} is working!")
    
    # Quick functionality test
    import numpy as np
    test_img = np.zeros((50, 50, 3), dtype=np.uint8)
    gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    st.success("✅ OpenCV operations work!")
    
except ImportError as e:
    st.error(f"❌ IMPORT ERROR: {e}")
    
    # Show what packages are available
    try:
        import pkg_resources
        installed = [str(d) for d in pkg_resources.working_set]
        opencv_pkgs = [p for p in installed if 'opencv' in p.lower()]
        
        if opencv_pkgs:
            st.write("**OpenCV packages found:**")
            for pkg in opencv_pkgs:
                st.write(f"- {pkg}")
        else:
            st.write("**No OpenCV packages found!**")
            
        # Show some other packages for comparison
        common_pkgs = ['numpy', 'pillow', 'streamlit']
        st.write("**Other packages:**")
        for pkg_name in common_pkgs:
            matching = [p for p in installed if pkg_name.lower() in p.lower()]
            if matching:
                st.write(f"- {matching[0]}")
            else:
                st.write(f"- {pkg_name}: NOT FOUND")
                
    except Exception as pkg_error:
        st.write(f"Could not check packages: {pkg_error}")
        
except Exception as e:
    st.error(f"❌ UNEXPECTED ERROR: {e}")

# File system check
st.subheader("📁 Files")
try:
    files = sorted(os.listdir('.'))
    st.write("**Current directory contents:**")
    for f in files[:10]:  # Show first 10 files
        st.write(f"- {f}")
    if len(files) > 10:
        st.write(f"... and {len(files) - 10} more files")
except Exception as e:
    st.write(f"Could not list files: {e}")

# Requirements check
if os.path.exists('requirements.txt'):
    st.subheader("📋 Requirements.txt")
    try:
        with open('requirements.txt', 'r') as f:
            req_content = f.read()
        
        if 'opencv-python-headless' in req_content:
            st.success("✅ opencv-python-headless found in requirements.txt")
        else:
            st.error("❌ opencv-python-headless NOT found in requirements.txt")
            
        st.code(req_content[:500])  # Show first 500 chars
        
    except Exception as e:
        st.error(f"Could not read requirements.txt: {e}")
else:
    st.error("❌ requirements.txt not found!")

st.subheader("🚀 Next Steps")
if "SUCCESS" in st.session_state.get('opencv_status', ''):
    st.balloons()
    st.success("🎉 OpenCV is working! You can now use your full app.")
else:
    st.write("""
    **If this test fails on Streamlit Cloud:**
    1. Check that `requirements.txt` contains `opencv-python-headless==4.8.1.78`
    2. Try clicking "Reboot app" in Streamlit Cloud menu
    3. Redeploy from scratch if needed
    4. Make sure all files are in repository root
    """)
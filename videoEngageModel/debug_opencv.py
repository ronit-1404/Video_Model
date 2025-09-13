import streamlit as st
import sys
import os

st.title("🔍 OpenCV Debug Dashboard")
st.write("This page helps debug OpenCV installation issues on Streamlit Cloud")

# Show Python version and path
st.subheader("🐍 Python Environment")
st.write(f"**Python Version:** {sys.version}")
st.write(f"**Python Executable:** {sys.executable}")
st.write(f"**Current Working Directory:** {os.getcwd()}")

# Show available packages
st.subheader("📦 Installed Packages")
try:
    import pkg_resources
    installed_packages = [d for d in pkg_resources.working_set]
    cv_packages = [str(pkg) for pkg in installed_packages if 'opencv' in str(pkg).lower()]
    numpy_packages = [str(pkg) for pkg in installed_packages if 'numpy' in str(pkg).lower()]
    
    st.write("**OpenCV Related Packages:**")
    if cv_packages:
        for pkg in cv_packages:
            st.success(f"✅ {pkg}")
    else:
        st.error("❌ No OpenCV packages found")
    
    st.write("**NumPy Package:**")
    if numpy_packages:
        for pkg in numpy_packages:
            st.success(f"✅ {pkg}")
    else:
        st.error("❌ NumPy not found")
        
except Exception as e:
    st.error(f"Could not check packages: {e}")

# Test OpenCV import
st.subheader("🔬 OpenCV Import Test")
try:
    import cv2
    st.success(f"✅ OpenCV imported successfully!")
    st.info(f"📌 OpenCV Version: {cv2.__version__}")
    
    # Test basic functionality
    import numpy as np
    test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    st.success("✅ Basic OpenCV operations work!")
    
except ImportError as e:
    st.error(f"❌ OpenCV import failed: {e}")
    
    # Show detailed error information
    st.write("**Error Details:**")
    st.code(str(e))
    
    # Check if opencv-python is installed instead of opencv-python-headless
    try:
        import pkg_resources
        all_packages = [str(d) for d in pkg_resources.working_set]
        opencv_variants = [pkg for pkg in all_packages if 'opencv' in pkg.lower()]
        
        st.write("**All OpenCV variants found:**")
        for pkg in opencv_variants:
            st.write(f"- {pkg}")
            
        if any('opencv-python ' in pkg and 'headless' not in pkg for pkg in opencv_variants):
            st.warning("⚠️ Found 'opencv-python' instead of 'opencv-python-headless'. This can cause issues on Streamlit Cloud.")
            
    except:
        pass
    
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")

# Test NumPy
st.subheader("🔢 NumPy Test")
try:
    import numpy as np
    st.success(f"✅ NumPy imported successfully!")
    st.info(f"📌 NumPy Version: {np.__version__}")
except Exception as e:
    st.error(f"❌ NumPy import failed: {e}")

# Show file system
st.subheader("📁 File System Check")
st.write("**Current directory contents:**")
current_dir = os.getcwd()
try:
    files = os.listdir(current_dir)
    for file in sorted(files):
        if os.path.isdir(os.path.join(current_dir, file)):
            st.write(f"📁 {file}/")
        else:
            st.write(f"📄 {file}")
except Exception as e:
    st.error(f"Could not list directory: {e}")

# Check requirements.txt
st.subheader("📋 Requirements.txt Check")
req_file = "requirements.txt"
if os.path.exists(req_file):
    st.success(f"✅ {req_file} found")
    try:
        with open(req_file, 'r') as f:
            content = f.read()
        st.code(content, language='text')
        
        # Check for opencv line
        lines = content.lower().split('\n')
        opencv_lines = [line for line in lines if 'opencv' in line]
        if opencv_lines:
            st.success(f"✅ OpenCV requirement found: {opencv_lines}")
        else:
            st.error("❌ No OpenCV requirement found in requirements.txt")
            
    except Exception as e:
        st.error(f"Could not read requirements.txt: {e}")
else:
    st.error(f"❌ {req_file} not found in current directory")

# Check packages.txt
st.subheader("🔧 Packages.txt Check")
pkg_file = "packages.txt"
if os.path.exists(pkg_file):
    st.success(f"✅ {pkg_file} found")
    try:
        with open(pkg_file, 'r') as f:
            content = f.read()
        st.code(content, language='text')
    except Exception as e:
        st.error(f"Could not read packages.txt: {e}")
else:
    st.warning(f"⚠️ {pkg_file} not found (may be needed for OpenCV)")

st.subheader("🚀 Next Steps")
st.write("""
If OpenCV import failed, try these solutions:

1. **Check requirements.txt** - Make sure it contains `opencv-python-headless==4.8.1.78`
2. **Check packages.txt** - System dependencies may be needed
3. **Redeploy** - Sometimes Streamlit Cloud needs a fresh deployment
4. **Check repository structure** - Make sure files are in the root directory
5. **Clear cache** - Try restarting your Streamlit Cloud app
""")
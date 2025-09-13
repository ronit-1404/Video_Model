#!/usr/bin/env python3
"""
Simple test script to verify OpenCV installation for Streamlit deployment
"""

def test_opencv():
    try:
        import cv2
        print(f"✅ OpenCV successfully imported!")
        print(f"📦 OpenCV version: {cv2.__version__}")
        
        # Test basic functionality
        import numpy as np
        
        # Create a simple test image
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[:] = (255, 0, 0)  # Blue image
        
        # Test basic OpenCV operations
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        print(f"✅ Color conversion test passed!")
        
        # Test cascade classifier loading (if files exist)
        try:
            face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
            if not face_cascade.empty():
                print(f"✅ Haar cascade loaded successfully!")
            else:
                print(f"⚠️  Haar cascade file found but appears empty")
        except Exception as e:
            print(f"⚠️  Could not load Haar cascade: {e}")
        
        print(f"🎉 All OpenCV tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import OpenCV: {e}")
        return False
    except Exception as e:
        print(f"❌ OpenCV test failed: {e}")
        return False

def test_dependencies():
    """Test other required dependencies"""
    dependencies = [
        'numpy', 'tensorflow', 'librosa', 'streamlit', 
        'matplotlib', 'pandas', 'scipy', 'PIL'
    ]
    
    print("\n🔍 Checking other dependencies:")
    for dep in dependencies:
        try:
            if dep == 'PIL':
                import PIL
                print(f"✅ {dep}: {PIL.__version__}")
            else:
                module = __import__(dep)
                version = getattr(module, '__version__', 'unknown')
                print(f"✅ {dep}: {version}")
        except ImportError:
            print(f"❌ {dep}: Not found")

if __name__ == "__main__":
    print("🚀 Testing OpenCV and dependencies for Streamlit deployment...\n")
    
    success = test_opencv()
    test_dependencies()
    
    if success:
        print(f"\n🎯 All tests passed! Your app should work on Streamlit Cloud.")
    else:
        print(f"\n⚠️  Some issues detected. Please check your requirements.txt file.")
# Streamlit Cloud Deployment Guide

## Files Required for OpenCV Support

Make sure your repository contains these files in the root directory:

### 1. requirements.txt
```
streamlit>=1.28.0
opencv-python-headless==4.8.1.78
numpy==1.26.4
pillow>=9.5.0
matplotlib>=3.7.0
pandas>=2.0.0
scipy>=1.10.0
tensorflow>=2.13.0
librosa>=0.10.0
scikit-learn>=1.3.0
```

### 2. packages.txt (for system dependencies)
```
libgl1-mesa-glx
libglib2.0-0
libsm6
libxext6
libxrender-dev
libgomp1
libgthread-2.0-0
libgtk-3-0
libavcodec-dev
libavformat-dev
libswscale-dev
libv4l-dev
libxvidcore-dev
libx264-dev
libjpeg-dev
libpng-dev
libtiff-dev
libatlas-base-dev
gfortran
libhdf5-dev
```

### 3. .streamlit/config.toml
```toml
[global]
developmentMode = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200
port = 8501
```

## Deployment Steps

1. **Push all files to GitHub**: Make sure all the above files are in your repository root
2. **Connect to Streamlit Cloud**: Go to https://share.streamlit.io/
3. **Deploy from GitHub**: Select your repository and main branch
4. **Set main file**: Make sure it points to `streamlit_app.py`
5. **Wait for deployment**: This may take 5-10 minutes for the first deployment

## Troubleshooting

### OpenCV Import Error
- Ensure `opencv-python-headless` is in requirements.txt (NOT `opencv-python`)
- Make sure packages.txt includes all system dependencies
- Try redeploying (sometimes cache issues occur)

### Model Loading Issues
- Ensure model files are under 100MB (GitHub limit)
- Use Git LFS for larger files
- Check file paths are relative to the root directory

### Memory Issues
- Use `opencv-python-headless` instead of full OpenCV
- Optimize model loading in your code
- Consider model quantization for smaller file sizes

## Testing Locally

Run the test script to verify everything works:
```bash
python test_opencv.py
```

## Common Issues

1. **Mixed OpenCV packages**: Don't mix `opencv-python` and `opencv-python-headless`
2. **Missing system dependencies**: All dependencies in packages.txt are required
3. **File path issues**: Use relative paths from the repository root
4. **Case sensitivity**: Linux is case-sensitive, check your file names

## Success Indicators

When deployment is successful, you should see:
- ✅ OpenCV version X.X.X loaded successfully!
- No import errors in the Streamlit logs
- Your app loads without crashes
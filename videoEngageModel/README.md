# Student Attention Detection - Organized Version

## Project Structure

- `notebooks/` - Jupyter notebooks for model development and experiments
- `scripts/` - Python scripts for running detection and inference
- `models/` - Pretrained and trained model files
- `data/` - Place for datasets (empty by default)
- `haarcascades/` - Haarcascade XML files for face/eye detection
- `samples/` - Sample video/audio files for testing

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd Student-Attention-Detection-StacksCompetition-Organized
   ```

2. **Install dependencies**
   - Make sure you have Python 3.8+ installed.
   - Install required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the main script**
   ```sh
   python scripts/live_video.py
   ```

4. **Explore Notebooks**
   - Open files in `notebooks/` using JupyterLab or VS Code.

## Notes
- Place your own data in the `data/` folder if needed.
- Update paths in scripts/notebooks if you move files.
- For Haarcascade files, ensure OpenCV is installed.

---

For any issues, open an issue or discussion on your GitHub repository.

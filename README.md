# RGB Thermal Overlay Algorithm

A professional web application for aligning thermal images with RGB images using advanced computer vision techniques. This application uses ORB feature detection and homography transformation to precisely align thermal images with their RGB counterparts.

## Features

- 🎯 **Precise Alignment**: Uses ORB feature detection and RANSAC-based homography for accurate image alignment
- ⚡ **Fast Processing**: Optimized algorithms ensure quick processing of your thermal and RGB image pairs
- 📦 **Easy Download**: Receive your aligned images in a convenient ZIP file
- 🛡️ **Secure & Private**: Your images are processed securely and never stored on our servers
- 💻 **Modern UI**: Beautiful, responsive interface built with modern web technologies

## Technology Stack

- **Backend**: Flask (Python)
- **Computer Vision**: OpenCV
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render & Vercel ready

## Local Development

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd "Task 1 - RGB Thermal Overlay Algorithm"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Deployment

### Deploying to Render

1. **Create a Render Account**: Sign up at [render.com](https://render.com)

2. **Create a New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration

3. **Configure Settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3

4. **Deploy**: Render will automatically deploy your application

5. **Your App URL**: Render will provide you with a URL like `https://your-app-name.onrender.com`

### Deploying to Vercel

**Note**: Vercel has limitations with OpenCV due to binary size. For full OpenCV support, Render is recommended.

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Deploy**:
```bash
vercel
```

3. **Follow the prompts** to configure your deployment

4. **Alternative**: Connect your GitHub repository to Vercel dashboard for automatic deployments

## Usage

1. **Upload Images**:
   - Upload your thermal image (format: `XXXX_T.JPG`)
   - Upload your corresponding RGB image (format: `XXXX_Z.JPG`)

2. **Process**:
   - Click "Process Images" button
   - Wait for the alignment algorithm to complete

3. **Download**:
   - Your processed images will be automatically downloaded as a ZIP file
   - The ZIP contains:
     - `aligned_AT.JPG`: The aligned thermal image
     - `original_Z.JPG`: The original RGB image

## Algorithm Details

The alignment process uses:
- **ORB (Oriented FAST and Rotated BRIEF)** feature detector for keypoint detection
- **Brute Force Matcher** with Hamming distance for feature matching
- **RANSAC** algorithm for robust homography estimation
- **Perspective Transformation** to warp the thermal image to match the RGB image

If feature matching fails, the system falls back to a simple resize operation.

## File Structure

```
.
├── app.py                 # Flask application
├── overlay_thermal.py     # Core alignment algorithm
├── templates/            # HTML templates
│   └── index.html
├── static/               # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── requirements.txt      # Python dependencies
├── render.yaml           # Render deployment config
├── vercel.json           # Vercel deployment config
├── Procfile              # Process file for Render
└── README.md            # This file
```

## License

This project is open source and available for use.

## Support

For issues or questions, please open an issue in the repository.


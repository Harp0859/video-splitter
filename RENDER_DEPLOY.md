# Deploy to Render - Simple Python Backend

## 🚀 Quick Deployment Steps

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/video-splitter.git
git push -u origin main
```

### 2. Deploy on Render

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure:**
   - **Name**: `video-splitter`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: `Free`

### 3. Update Frontend

After deployment, update the API URL in `index.html`:

```javascript
// Change this line in index.html:
const API_BASE_URL = 'https://your-app-name.onrender.com';
```

## ⚠️ Important Notes for Render

### **FFmpeg Issue on Render Free Tier**
- **Problem**: Render's free tier doesn't have FFmpeg pre-installed
- **Solution**: You have 2 options:

#### Option 1: Use MoviePy (Python-based)
Replace FFmpeg with MoviePy in your code:

```python
# In app.py, replace the ffmpeg_split_video function
from moviepy.editor import VideoFileClip
import os

def moviepy_split_video(video_path, output_dir, chunk_duration=60, overlap=10):
    """Split video using MoviePy instead of FFmpeg"""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Load video
    video = VideoFileClip(video_path)
    duration = video.duration
    
    chunk_paths = []
    start_time = 0
    chunk_num = 1
    
    while start_time < duration:
        end_time = min(start_time + chunk_duration, duration)
        output_path = os.path.join(output_dir, f"chunk_{chunk_num:03d}.mp4")
        
        # Extract chunk
        chunk = video.subclip(start_time, end_time)
        chunk.write_videofile(output_path, codec='libx264', audio_codec='aac')
        chunk.close()
        
        chunk_paths.append(output_path)
        start_time += chunk_duration - overlap
        chunk_num += 1
        
        if start_time >= duration:
            break
    
    video.close()
    return chunk_paths
```

#### Option 2: Upgrade to Paid Plan
- Render's paid plans support custom buildpacks with FFmpeg
- More reliable but costs money

## 📁 Files for Deployment

Your project structure:
```
video_splitter/
├── app.py              # Flask backend
├── index.html          # Frontend
├── requirements.txt    # Python dependencies
├── render.yaml        # Render config
├── Procfile           # Process file
└── README.md          # Documentation
```

## 🔧 Local Testing (Working!)

Your local setup is perfect:
- ✅ Flask server running on localhost:5000
- ✅ FFmpeg working perfectly
- ✅ Video splitting successful
- ✅ ZIP download working

## 🌐 Production Deployment

1. **Push code to GitHub**
2. **Deploy on Render**
3. **Update frontend API URL**
4. **Test with small video files first**

## 💡 Recommendation

For the **free tier**, I recommend using **MoviePy** instead of FFmpeg since it's pure Python and works on Render without additional setup.

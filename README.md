# Video Splitter

A web-based video splitting tool that uses FFmpeg to split videos into chunks with configurable overlap. The backend is built with Python Flask and can be deployed to Render.

## Features

- 🎬 Upload video files (MP4, AVI, MOV, MKV, WebM, FLV, WMV)
- ⚙️ Configure chunk duration and overlap
- 🔪 Fast video splitting using FFmpeg (lossless, no re-encoding)
- 📦 Automatic ZIP file generation and download
- 🧹 Automatic cleanup of temporary files
- 🌐 Web-based interface

## Local Development

### Prerequisites

- Python 3.8+
- FFmpeg installed on your system
- pip (Python package manager)

### Installation

1. Clone or download this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure FFmpeg is installed:
   - **Windows**: Download from https://ffmpeg.org/download.html
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian)

4. Run the Flask server:
   ```bash
   python app.py
   ```

5. Open `index.html` in your browser

## Deployment to Render

### Method 1: Using Render Dashboard

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3
   - **Plan**: Free

### Method 2: Using render.yaml

1. Push your code to GitHub
2. In Render Dashboard, click "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically detect the `render.yaml` file

### Important Notes for Render

- Render's free tier has limitations on file size and processing time
- For production use, consider upgrading to a paid plan
- The free tier may sleep after inactivity

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /upload` - Upload video file
- `POST /split` - Split video into chunks
- `GET /download/<filename>` - Download ZIP file
- `DELETE /cleanup/<file_id>` - Clean up temporary files

## Usage

1. **Upload Video**: Select a video file using the file input
2. **Configure Settings**: Set chunk duration and overlap
3. **Split Video**: Click "Split Video & Download ZIP"
4. **Download**: The ZIP file will be automatically downloaded

## File Structure

```
video_splitter/
├── app.py              # Flask backend server
├── index.html          # Frontend web interface
├── requirements.txt    # Python dependencies
├── render.yaml        # Render deployment config
├── Procfile           # Process file for deployment
└── README.md          # This file
```

## Troubleshooting

### Backend Issues

- **FFmpeg not found**: Make sure FFmpeg is installed and in your PATH
- **Port already in use**: Change the port in `app.py` (line 95)
- **CORS errors**: Check that Flask-CORS is properly installed

### Frontend Issues

- **Cannot connect to backend**: Update the `API_BASE_URL` in `index.html`
- **Upload fails**: Check file size limits and supported formats
- **Download fails**: Check browser download settings

## Supported Video Formats

- MP4
- AVI
- MOV
- MKV
- WebM
- FLV
- WMV

## Performance Notes

- Uses FFmpeg's `-c copy` flag for lossless, fast splitting
- No video re-encoding = much faster processing
- Memory usage scales with video file size
- Processing time depends on video duration and chunk count

## License

MIT License - feel free to use and modify as needed.

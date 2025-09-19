import os
import math
import subprocess
import tempfile
import zipfile
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
import subprocess
import os

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
CHUNKS_FOLDER = 'chunks'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv'}

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHUNKS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ffmpeg_split_video(video_path, output_dir="video_chunks", chunk_duration=60, overlap=10):
    """
    Super-fast video splitter using FFmpeg (lossless, no re-encoding).
    
    Args:
        video_path (str): Path to your video file.
        output_dir (str): Directory where the chunks will be saved.
        chunk_duration (int): Duration of each chunk in seconds.
        overlap (int): Overlap between chunks in seconds.
    
    Returns:
        list: Paths of generated video chunks.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"❌ Video file not found: {video_path}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Get video duration using FFmpeg
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", video_path
    ]
    video_duration = float(subprocess.check_output(cmd).decode().strip())
    
    print(f"🎬 Splitting: {os.path.basename(video_path)}")
    print(f"📁 Output: {output_dir}")
    print(f"⏱️ Duration: {video_duration/60:.1f} mins ({video_duration:.1f}s)")
    print(f"📦 Chunk size: {chunk_duration}s with {overlap}s overlap\n")
    
    chunk_paths = []
    start_time = 0
    chunk_num = 1
    
    while start_time < video_duration:
        end_time = min(start_time + chunk_duration, video_duration)
        output_path = os.path.join(output_dir, f"chunk_{chunk_num:03d}.mp4")
        
        print(f"🔹 Chunk {chunk_num} → {start_time:.1f}s → {end_time:.1f}s")
        
        # Build FFmpeg command (no re-encoding → super fast)
        cmd = [
            "ffmpeg", "-y", "-ss", str(start_time), "-to", str(end_time),
            "-i", video_path, "-c", "copy", output_path
        ]
        
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        chunk_paths.append(output_path)
        print(f"✅ Created {output_path}")
        
        # Move to next start time considering overlap
        start_time += chunk_duration - overlap
        chunk_num += 1
        
        if start_time >= video_duration:
            break
    
    print(f"\n✅ Done! Created {len(chunk_paths)} chunks in '{output_dir}'\n")
    return chunk_paths

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api')
def api_info():
    return jsonify({
        "message": "Video Splitter API",
        "status": "running",
        "endpoints": {
            "POST /upload": "Upload video file",
            "POST /split": "Split video into chunks",
            "GET /health": "Health check"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{file_id}.{file_extension}"
        
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        return jsonify({
            "message": "File uploaded successfully",
            "file_id": file_id,
            "filename": filename,
            "file_path": file_path
        })
    
    return jsonify({"error": "Invalid file type"}), 400

@app.route('/split', methods=['POST'])
def split_video():
    data = request.get_json()
    
    if not data or 'file_id' not in data:
        return jsonify({"error": "file_id is required"}), 400
    
    file_id = data['file_id']
    chunk_duration = data.get('chunk_duration', 60)
    overlap = data.get('overlap', 10)
    
    # Find the uploaded file
    file_path = None
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.startswith(file_id):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            break
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    try:
        # Create unique output directory for this split
        output_dir = os.path.join(CHUNKS_FOLDER, f"{file_id}_chunks")
        
        # Split the video
        chunk_paths = ffmpeg_split_video(
            video_path=file_path,
            output_dir=output_dir,
            chunk_duration=chunk_duration,
            overlap=overlap
        )
        
        # Create ZIP file
        zip_filename = f"{file_id}_video_chunks.zip"
        zip_path = os.path.join(CHUNKS_FOLDER, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for chunk_path in chunk_paths:
                zipf.write(chunk_path, os.path.basename(chunk_path))
        
        return jsonify({
            "message": "Video split successfully",
            "chunk_count": len(chunk_paths),
            "zip_filename": zip_filename,
            "download_url": f"/download/{zip_filename}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(CHUNKS_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

@app.route('/cleanup/<file_id>', methods=['DELETE'])
def cleanup_files(file_id):
    """Clean up uploaded file and generated chunks"""
    try:
        # Remove uploaded file
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.startswith(file_id):
                os.remove(os.path.join(UPLOAD_FOLDER, filename))
                break
        
        # Remove chunks directory
        chunks_dir = os.path.join(CHUNKS_FOLDER, f"{file_id}_chunks")
        if os.path.exists(chunks_dir):
            import shutil
            shutil.rmtree(chunks_dir)
        
        # Remove ZIP file
        zip_file = os.path.join(CHUNKS_FOLDER, f"{file_id}_video_chunks.zip")
        if os.path.exists(zip_file):
            os.remove(zip_file)
        
        return jsonify({"message": "Files cleaned up successfully"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

# Single Service Deployment on Render

## 🎯 **What You Get:**
- **One URL** for everything: `https://your-app.onrender.com`
- **Frontend** served at the root `/`
- **API** available at `/upload`, `/split`, `/health`, etc.
- **No CORS issues** - everything on same domain

## 🚀 **Deployment Steps:**

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Single service video splitter"
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

### 3. Access Your App
- **Frontend**: `https://your-app-name.onrender.com`
- **API Info**: `https://your-app-name.onrender.com/api`
- **Health Check**: `https://your-app-name.onrender.com/health`

## ✅ **What's Working Locally:**
- ✅ **Single service** serving both frontend and API
- ✅ **Frontend** loads at `http://localhost:5000/`
- ✅ **API** works at `http://localhost:5000/upload`, `/split`, etc.
- ✅ **No CORS issues** - same origin

## 📁 **File Structure:**
```
video_splitter/
├── app.py              # Flask app (serves HTML + API)
├── index.html          # Frontend (served by Flask)
├── requirements.txt    # Python dependencies
├── render.yaml        # Render config
└── Procfile           # Process file
```

## 🔧 **How It Works:**
1. **User visits** `https://your-app.onrender.com`
2. **Flask serves** `index.html` (frontend)
3. **Frontend makes API calls** to same domain
4. **No CORS issues** - everything on same origin

## ⚠️ **FFmpeg on Render Free Tier:**
- **Problem**: Render free tier doesn't have FFmpeg
- **Solutions**:
  1. **Upgrade to paid plan** (has FFmpeg)
  2. **Use MoviePy** (pure Python, works on free tier)

## 🎉 **Benefits of Single Service:**
- ✅ **Simpler deployment** - one service only
- ✅ **No CORS issues** - same domain
- ✅ **Easier to manage** - one URL
- ✅ **Cost effective** - one service instead of two

## 🧪 **Test Locally:**
Your local setup is working perfectly:
- Frontend: `http://localhost:5000/`
- API: `http://localhost:5000/health`
- Video splitting: Working perfectly!

Ready to deploy! 🚀

# Local Testing Guide

Test ResuMAX locally without paying for cloud resources.

## Setup (One-time)

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements-dev.txt
```

2. **Download the AI model (80MB):**
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

3. **Set environment variables:**
```bash
# Create .env file (optional for local testing)
echo "GCS_BUCKET_NAME=test-bucket" > .env
echo "GOOGLE_CLOUD_PROJECT=test-project" >> .env
```

## Running Locally

### Option 1: GUI (Recommended for Testing)

**Terminal 1 - Start Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8080
```
Leave this running. You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8080
```

**Terminal 2 - Start GUI:**
```bash
cd backend
streamlit run local_gui.py
```

This will open `http://localhost:8501` in your browser with the testing GUI.

### Option 2: API Testing (curl)

**Start backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8080
```

**Test health endpoint:**
```bash
curl http://localhost:8080/health
```

**Upload resume:**
```bash
curl -X POST http://localhost:8080/upload-resume \
  -F "file=@/path/to/your/resume.pdf" \
  -F "user_id=test-user-123"
```

## GUI Features

- ✅ Upload resume (PDF or DOCX)
- ✅ Parse and view extracted data
- ✅ Enter job description
- ✅ Select industry (or auto-detect)
- ✅ See before/after scores
- ✅ View optimized bullets and skills
- ✅ Download optimized PDF

## Notes

- **No cloud costs** - Everything runs on your machine
- **Data is not persisted** - Restarts will clear data (no database in local mode)
- **Storage doesn't work locally** - File upload/download won't persist to Google Cloud Storage
- Test with your actual resume to see how the semantic matching works!

## Troubleshooting

**"Connection error"** - Make sure backend is running on port 8080

**"Module not found"** - Run `pip install -r requirements-dev.txt`

**Backend crashes** - Check you have enough RAM (sentence-transformers needs ~500MB)

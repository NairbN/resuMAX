# ResuMAX Local Testing Guide

Quick guide to test the resume optimizer locally before deploying.

## Setup (First Time Only)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Download AI Model (~80MB)
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

This downloads the semantic matching model. First backend startup will be faster after this.

---

## Testing

### Method 1: Desktop GUI (Recommended)

**Terminal 1 - Start Backend:**
```bash
cd backend
./start_backend.sh
```

Wait for: `✅ Model loaded and ready!`

**Terminal 2 - Start Desktop GUI:**
```bash
cd backend
python desktop_gui.py
```

A window will pop up. You can:
1. Set auth token (just type "test" for local testing)
2. Upload your resume PDF
3. Paste a job description
4. Click "Optimize Resume"
5. See before/after scores!

### Method 2: API Testing (curl)

**Start backend:**
```bash
cd backend
LOCAL_TESTING=true python -m uvicorn app.main:app --reload --port 8080
```

**Test health endpoint:**
```bash
curl http://localhost:8080/health
```

**Upload resume:**
```bash
curl -X POST http://localhost:8080/upload-resume \
  -H "Authorization: Bearer test-token" \
  -F "file=@RyleyMao_CV.pdf"
```

---

## What Gets Tested

✅ **Resume Parsing** - Extracts bullets, skills, education
✅ **Semantic Matching** - Measures similarity with sentence-transformers
✅ **Structure Preservation** - Keeps format, never adds bullets
✅ **Industry Detection** - Auto-detects tech/finance/healthcare/etc
✅ **Before/After Scoring** - Shows improvement percentage

---

## Troubleshooting

### "Connection error" in GUI
- Make sure backend is running (`./start_backend.sh`)
- Backend should show: `✅ Model loaded and ready!`

### "Auth Error"
- In the GUI, set token to "test" (any value works in local mode)
- Or run backend with: `LOCAL_TESTING=true`

### Backend takes 30-60 seconds on first request
- This is normal! The sentence-transformers model loads on first use
- Subsequent requests will be fast (2-5 seconds)

### "Firebase Admin initialization failed"
- Ignore this for local testing
- Make sure `LOCAL_TESTING=true` is set
- Auth will be bypassed automatically

---

## Test with Your Resume

1. Use your actual resume PDF
2. Find a real job description on LinkedIn/Indeed
3. Paste the full job description (not just title)
4. See how the semantic matching works!

**Example Job Description:**
```
Backend Engineer at TechCorp

We're seeking a backend engineer with strong Python skills.
Build scalable APIs using FastAPI or Django. Experience with
cloud platforms (AWS/GCP) and databases (PostgreSQL, MongoDB).
Knowledge of Docker, Kubernetes, and CI/CD pipelines preferred.
```

The optimizer will:
- Rank your bullets by relevance to this job
- Highlight Python, API, and cloud experience
- Reorder to put most relevant skills first
- Show you the improvement score

---

## No Cloud Costs

Everything runs locally:
- ✅ $0 cost
- ✅ Fast testing
- ✅ No internet needed (after model download)
- ✅ Private - your resume stays on your machine

When ready to deploy, use:
```bash
gcloud builds submit
```

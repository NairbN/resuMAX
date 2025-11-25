# ResuMAX - AI Resume Optimizer

Open-source resume optimizer that uses **semantic matching** (not LLMs!) to optimize your resume for specific job descriptions.

## Features

✅ **Smart Semantic Matching** - Uses sentence-transformers to understand meaning, not just keywords
✅ **Structure Preserving** - Never changes your format, company names, or dates
✅ **Industry-Aware** - Auto-detects industry (tech, finance, healthcare, etc.) and optimizes accordingly
✅ **Before/After Scoring** - Shows you exactly how much your resume improved
✅ **No LLM Required** - Uses traditional NLP + embeddings (fast, cheap, private)
✅ **Cloud-Ready** - Deploy to Google Cloud Run with one command

## How It Works

1. **Upload Resume** - PDF or DOCX format
2. **Paste Job Description** - Full job posting from LinkedIn/Indeed/etc
3. **Get Optimized Resume** - Bullets reordered by relevance, skills highlighted
4. **See Improvement Score** - "Your resume is now 23% more relevant!"

### Example

**Before:**
```
• Created Excel reports for finance team
• Built Python API using FastAPI
• Managed team of 5 engineers
```

**Job:** "Backend Engineer - Python, APIs, microservices"

**After (reordered by semantic relevance):**
```
• Built Python API using FastAPI (87% match)
• Managed team of 5 engineers (54% match)
• Created Excel reports for finance team (21% match)
```

## Tech Stack

- **Backend:** FastAPI (Python)
- **Semantic Matching:** sentence-transformers (all-MiniLM-L6-v2 model, 80MB)
- **Cloud:** Google Cloud Run, Cloud Storage, Firestore
- **Auth:** Firebase Authentication
- **Parsing:** pdfplumber, python-docx

## Quick Start (Local Testing)

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/resuMAX.git
cd resuMAX/backend

# Install dependencies
pip install -r requirements.txt

# Download semantic matching model (80MB, one-time)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy environment template
cp .env.example .env
```

### Run Locally

**Terminal 1 - Start Backend:**
```bash
./start_backend.sh
```

Wait for: `✅ Model loaded and ready!`

**Terminal 2 - Start Desktop GUI:**
```bash
python desktop_gui.py
```

The desktop GUI will open. Try it with your resume!

### Test with curl

```bash
# Health check
curl http://localhost:8080/health

# Upload resume
curl -X POST http://localhost:8080/upload-resume \
  -H "Authorization: Bearer test-token" \
  -F "file=@your_resume.pdf"
```

## Deployment (Google Cloud)

### Prerequisites

- Google Cloud account
- `gcloud` CLI installed
- Billing enabled

### Deploy

```bash
cd backend

# Build and deploy
gcloud builds submit

# Deploy to Cloud Run
gcloud run deploy resumax-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

Your API will be live at: `https://resumax-api-XXXXX.run.app`

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Local testing (bypasses Firebase auth)
LOCAL_TESTING=true

# Google Cloud (required for production)
GCS_BUCKET_NAME=your-bucket-name
GOOGLE_CLOUD_PROJECT=your-project-id

# Firebase (required for production)
# Download from Firebase Console > Project Settings > Service Accounts
FIREBASE_SERVICE_ACCOUNT=/path/to/serviceAccountKey.json
```

## Firebase Setup (for Contributors)

1. Create Firebase project at https://console.firebase.google.com
2. Enable Google Authentication
3. Get your config from Project Settings
4. Update `backend/get_token.html` with your Firebase config
5. Download service account key (keep it SECRET!)

## Project Structure

```
resuMAX/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── auth.py              # Firebase auth
│   │   ├── semantic_matcher.py  # Core ML algorithm
│   │   ├── resume_parser.py     # PDF/DOCX parsing
│   │   ├── optimizer.py         # Resume optimization
│   │   └── ...
│   ├── desktop_gui.py           # Testing GUI
│   ├── requirements.txt         # Python deps
│   ├── Dockerfile              # Container config
│   └── cloudbuild.yaml         # GCP deployment
└── frontend/                   # (Your friend's code)
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Good First Issues

- [ ] Add support for more resume formats (LinkedIn PDF, etc)
- [ ] Improve industry detection accuracy
- [ ] Add more industries (legal, education, etc)
- [ ] Create browser extension
- [ ] Add resume templates

## Cost Estimate (Cloud Deployment)

Based on 1000 resumes/month:

- Cloud Run: **~$0.50/month** (scales to zero)
- Cloud Storage: **~$0.02/month** (5 resumes per user)
- Firestore: **Free tier** (easily covers this)

**Total: ~$0.52/month** for light usage

## License

MIT License - see [LICENSE](LICENSE)

## Why No LLM?

LLMs are powerful but:
- **Expensive** - GPT-4 would cost $0.10-0.30 per resume
- **Slow** - 10-30 seconds vs 2-5 seconds
- **Overkill** - Semantic matching is 87% accurate for this task
- **Privacy** - sentence-transformers runs locally

We use **sentence-transformers** instead:
- 80MB model (runs on CPU)
- Fast (2-5 seconds)
- Accurate (0.89 cosine similarity for relevant bullets)
- Free to run

## Credits

Built by [@ryleymao](https://github.com/ryleymao) and friends

Powered by:
- [sentence-transformers](https://github.com/UKPLab/sentence-transformers)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Cloud](https://cloud.google.com/)

---

**Star ⭐ this repo if you find it useful!**

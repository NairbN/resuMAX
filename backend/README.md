# resuMAX Backend API

Clean, production-ready backend for resume optimization using semantic similarity matching.

## Architecture Overview

```
backend/
├── app/
│   ├── main.py                    # FastAPI application & API routes
│   ├── optimizer.py               # Core resume optimization logic using semantic similarity
│   ├── resume_layout_engine.py    # PDF generation with HTML/CSS templates
│   ├── semantic_matcher.py        # Sentence embeddings & similarity scoring
│   ├── bullet_classifier.py       # Categorize bullets (technical, leadership, impact)
│   ├── industries.py              # Industry-specific configurations
│   ├── resume_parser.py           # Parse PDF/DOCX resumes
│   ├── job_parser.py              # Extract keywords from job descriptions
│   ├── smart_parser.py            # Advanced resume parsing logic
│   ├── auth.py                    # Firebase authentication
│   ├── database.py                # Firestore database operations
│   └── storage.py                 # Google Cloud Storage operations
├── requirements.txt               # Python dependencies
├── run_server.sh                  # Start server with proper environment
└── .env.example                   # Environment variable template
```

## Key Features

### 1. Semantic Similarity Matching (Not Just Keywords!)
- Uses sentence-transformers (all-MiniLM-L6-v2) for deep semantic understanding
- Scores resume bullets based on meaning, not just keyword matches
- Reorders bullets within each job/project by relevance to job description

### 2. Professional PDF Generation
- HTML/CSS-based layout engine using WeasyPrint
- Automatic one-page fitting (removes lowest-scored bullets until fits)
- Professional formatting (Times New Roman, proper spacing)

### 3. Industry-Aware Optimization
- Auto-detects industry from job description
- Custom configurations for Software Engineering, Data Science, Product Management, etc.

## Setup Instructions

### Prerequisites
- Python 3.13
- Homebrew (for macOS)
- Google Cloud project with Firestore and Cloud Storage

### Step 1: Install System Dependencies (macOS)

```bash
brew install cairo pango gdk-pixbuf gobject-introspection
```

### Step 2: Set up Python Environment

```bash
# Create virtual environment (if not exists)
python3 -m venv venv

# Install dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your Google Cloud credentials
```

### Step 4: Run the Server

```bash
# Use the provided script (sets DYLD_LIBRARY_PATH automatically)
./run_server.sh

# Or manually:
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /health
```

### Upload Resume
```
POST /upload-resume
Content-Type: multipart/form-data
Authorization: Bearer <firebase-token>

Body:
  file: PDF or DOCX resume
```

### Optimize Resume
```
POST /job-description
Content-Type: application/json
Authorization: Bearer <firebase-token>

Body:
{
  "resume_id": "uuid",
  "job_description": "Full job description text...",
  "job_title": "Software Engineer" (optional),
  "company": "Company Name" (optional)
}
```

### Download Resume
```
GET /download-resume/{resume_id}?version=optimized
Authorization: Bearer <firebase-token>
```

### List Resumes
```
GET /resumes
Authorization: Bearer <firebase-token>
```

### Delete Resume
```
DELETE /resume/{resume_id}
Authorization: Bearer <firebase-token>
```

## Code Quality

### Recent Cleanup (Nov 2025)
- ✅ Removed 415 lines of unused code (structure_preserving_optimizer.py)
- ✅ Removed duplicate PDF generation functions
- ✅ Fixed deprecated datetime.utcnow() calls
- ✅ Removed duplicate imports
- ✅ Cleaned up unused dependencies

### Architecture Decisions

**Why WeasyPrint over ReportLab?**
- Automatic text wrapping and layout
- CSS-based styling (easier to maintain)
- Consistent one-page output
- Deterministic rendering

**Why Sentence Transformers?**
- Deep semantic understanding beyond keyword matching
- Pre-trained on 1B+ sentence pairs
- Fast inference (CPU-friendly)
- Industry standard for semantic similarity

## Troubleshooting

### WeasyPrint Error: "cannot load library 'gobject-2.0-0'"
**Solution:** Set the library path before running:
```bash
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
```
Or use the provided `./run_server.sh` script.

### Python Dependencies Install Error
**Solution:** Use the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Model Download Timeout
**Solution:** The first run downloads the sentence-transformers model (~90MB). This is cached for subsequent runs.

## Development

### Adding New Features

1. **New API Endpoint**: Add route in `main.py`
2. **New Optimization Logic**: Extend `optimizer.py` or `semantic_matcher.py`
3. **New Industry**: Add configuration in `industries.py`

### Testing

```bash
# Run backend tests (when available)
pytest

# Test PDF generation manually
venv/bin/python -c "from app.resume_layout_engine import generate_optimized_resume_html; print('PDF generation works')"
```

## Performance

- **First request**: ~3-5s (model loading)
- **Subsequent requests**: ~1-2s (cached model)
- **PDF generation**: ~500ms (one-page resume)
- **Max resume size**: 5MB

## Security

- Firebase authentication required for all user endpoints
- User data isolated in Firestore (userId-based queries)
- Maximum 5 resumes per user
- Secure file upload with content-type validation

## License

MIT

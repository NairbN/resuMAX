#!/bin/bash
# Start backend with LOCAL_TESTING mode enabled
# This bypasses Firebase auth verification for local development

echo "🚀 Starting ResuMAX Backend (Local Testing Mode)"
echo "================================================"
echo ""
echo "Features enabled:"
echo "  ✅ Semantic matching with sentence-transformers"
echo "  ✅ Resume parsing (PDF, DOCX)"
echo "  ✅ Job description optimization"
echo "  ⚠️  Auth bypassed (LOCAL_TESTING=true)"
echo ""
echo "Backend will be available at: http://localhost:8080"
echo "Press Ctrl+C to stop"
echo ""

# Set environment variable for local testing
export LOCAL_TESTING=true

# Start uvicorn
python -m uvicorn app.main:app --reload --port 8080

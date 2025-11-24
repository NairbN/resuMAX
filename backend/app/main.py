from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
from typing import Optional
import uuid
from datetime import datetime

# Import our processing modules (we'll create these)
from app.resume_parser import parse_resume
from app.job_parser import parse_job_description
from app.optimizer import optimize_resume
from app.storage import upload_to_gcs, download_from_gcs
from app.database import save_resume_metadata, get_resume_metadata

app = FastAPI(title="resuMAX API", version="1.0.0")

# CORS - allow your frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobDescriptionRequest(BaseModel):
    user_id: str
    resume_id: str
    job_description: str
    job_title: Optional[str] = None
    company: Optional[str] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "resuMAX API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check for Cloud Run"""
    return {"status": "ok"}

@app.post("/upload-resume")
async def upload_resume(
    user_id: str,
    file: UploadFile = File(...)
):
    """
    Upload a resume (PDF/DOCX) and store it in Cloud Storage.

    Args:
        user_id: Firebase Auth user ID
        file: Resume file (PDF or DOCX)

    Returns:
        resume_id, original_file_url, parsed_data
    """
    try:
        # Validate file type
        allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")

        # Generate unique resume ID
        resume_id = str(uuid.uuid4())

        # Read file content
        content = await file.read()

        # Upload to Cloud Storage (original folder)
        bucket_name = os.getenv("GCS_BUCKET_NAME", "resumax-resumes")
        file_extension = file.filename.split('.')[-1]
        gcs_path = f"resumes/{user_id}/original/{resume_id}.{file_extension}"

        file_url = upload_to_gcs(
            bucket_name=bucket_name,
            destination_path=gcs_path,
            content=content,
            content_type=file.content_type
        )

        # Parse the resume to extract bullets and structure
        parsed_data = parse_resume(content, file.content_type)

        # Save metadata to Firestore (only original resume info, max 5 resumes)
        metadata = {
            "userId": user_id,
            "resumeId": resume_id,
            "originalFile": gcs_path,
            "originalFileName": file.filename,
            "uploadedAt": datetime.utcnow().isoformat(),
            "bulletCount": len(parsed_data.get("bullets", [])),
            "contactEmail": parsed_data.get("contact_info", {}).get("email", "")
        }

        try:
            save_resume_metadata(resume_id, metadata)
        except Exception as e:
            if "Resume limit reached" in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Resume limit reached. You can have maximum 5 resumes. Please delete old resumes first."
                )

        return {
            "resume_id": resume_id,
            "original_file_url": file_url,
            "parsed_data": {
                "bullet_count": len(parsed_data.get("bullets", [])),
                "sections": list(parsed_data.get("sections", {}).keys())
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading resume: {str(e)}")

@app.post("/job-description")
async def process_job_description(request: JobDescriptionRequest):
    """
    Process job description and optimize the resume based on it.

    Args:
        request: Contains user_id, resume_id, job_description, optional job_title/company

    Returns:
        optimized_file_url, relevance_scores
    """
    try:
        # Get resume metadata from Firestore
        metadata = get_resume_metadata(request.resume_id, request.user_id)
        if not metadata:
            raise HTTPException(status_code=404, detail="Resume not found")

        # Download original resume from Cloud Storage
        bucket_name = os.getenv("GCS_BUCKET_NAME", "resumax-resumes")
        original_content = download_from_gcs(
            bucket_name=bucket_name,
            source_path=metadata["originalFile"]
        )

        # Parse the original resume
        content_type = "application/pdf" if metadata["originalFile"].endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        parsed_resume = parse_resume(original_content, content_type)

        # Parse job description
        job_keywords = parse_job_description(request.job_description)

        # Optimize the resume (reorder bullets, highlight relevant skills)
        optimized_resume, scores = optimize_resume(
            parsed_resume=parsed_resume,
            job_keywords=job_keywords,
            original_content=original_content,
            content_type=content_type
        )

        # Upload optimized resume to Cloud Storage
        file_extension = "pdf"  # Always output as PDF
        optimized_path = f"resumes/{request.user_id}/optimized/{request.resume_id}_optimized.{file_extension}"

        optimized_url = upload_to_gcs(
            bucket_name=bucket_name,
            destination_path=optimized_path,
            content=optimized_resume,
            content_type="application/pdf"
        )

        # Update metadata in Firestore
        metadata.update({
            "optimizedFile": optimized_path,
            "jobDescription": request.job_description,
            "jobTitle": request.job_title,
            "company": request.company,
            "optimizedAt": datetime.utcnow().isoformat(),
            "status": "optimized",
            "relevanceScore": scores.get("overall_score", 0)
        })
        save_resume_metadata(request.resume_id, metadata)

        return {
            "resume_id": request.resume_id,
            "optimized_file_url": optimized_url,
            "relevance_scores": scores
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing resume: {str(e)}")

@app.get("/download-resume/{resume_id}")
async def download_resume(resume_id: str, user_id: str, version: str = "optimized"):
    """
    Download a resume (original or optimized).

    Args:
        resume_id: The resume ID
        user_id: Firebase Auth user ID (for authorization)
        version: "original" or "optimized" (default: optimized)

    Returns:
        Streaming file download
    """
    try:
        # Get resume metadata
        metadata = get_resume_metadata(resume_id)
        if not metadata:
            raise HTTPException(status_code=404, detail="Resume not found")

        if metadata["userId"] != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized access to resume")

        # Determine which file to download
        if version == "optimized":
            if "optimizedFile" not in metadata:
                raise HTTPException(status_code=404, detail="Optimized resume not available")
            gcs_path = metadata["optimizedFile"]
        else:
            gcs_path = metadata["originalFile"]

        # Download from Cloud Storage
        bucket_name = os.getenv("GCS_BUCKET_NAME", "resumax-resumes")
        content = download_from_gcs(
            bucket_name=bucket_name,
            source_path=gcs_path
        )

        # Determine content type
        content_type = "application/pdf" if gcs_path.endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        return StreamingResponse(
            iter([content]),
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={resume_id}_{version}.pdf"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading resume: {str(e)}")

@app.get("/resumes/{user_id}")
async def list_resumes(user_id: str):
    """
    List all resumes for a user.

    Args:
        user_id: Firebase Auth user ID

    Returns:
        List of resume metadata
    """
    try:
        from app.database import list_user_resumes
        resumes = list_user_resumes(user_id)
        return {"resumes": resumes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing resumes: {str(e)}")

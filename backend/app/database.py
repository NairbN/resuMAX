"""
Firestore Database Module

Handles resume metadata storage and retrieval in Firestore.
"""

from typing import Dict, List, Optional, Any
from google.cloud import firestore
from datetime import datetime


def get_firestore_client():
    """
    Get Firestore client.

    The client automatically uses credentials from:
        - Cloud Run environment (default service account)
        - GOOGLE_APPLICATION_CREDENTIALS environment variable
        - gcloud auth application-default login
    """
    return firestore.Client()


def save_resume_metadata(resume_id: str, metadata: Dict[str, Any]) -> None:
    """
    Save or update resume metadata in Firestore.

    LIMIT: Users can have max 5 resumes at a time.

    Args:
        resume_id: Unique resume identifier
        metadata: Resume metadata dictionary

    Collection structure:
        users/
            {userId}/
                resumes/
                    {resume_id}/
                        resumeId: str
                        originalFileName: str
                        originalFile: str (GCS path)
                        uploadedAt: str (ISO timestamp)
                        bulletCount: int
                        contactEmail: str

    Example:
        save_resume_metadata("res123", {
            "userId": "user123",
            "resumeId": "res123",
            "originalFileName": "ryley_resume.pdf",
            "originalFile": "gs://bucket/resumes/user123/res123.pdf",
            "uploadedAt": "2025-11-24T00:00:00Z",
            "bulletCount": 17,
            "contactEmail": "rymao_@outlook.com"
        })
    """

    try:
        db = get_firestore_client()

        user_id = metadata.get("userId")
        if not user_id:
            raise Exception("userId is required in metadata")

        # Check resume limit (5 max)
        existing_resumes = list_user_resumes(user_id)
        if len(existing_resumes) >= 5 and resume_id not in [r['resumeId'] for r in existing_resumes]:
            raise Exception("Resume limit reached. Users can have maximum 5 resumes. Delete old resumes first.")

        # Save to user's resumes subcollection
        user_resume_ref = db.collection("users").document(user_id).collection("resumes").document(resume_id)
        user_resume_ref.set(metadata, merge=True)

    except Exception as e:
        raise Exception(f"Failed to save resume metadata: {str(e)}")


def get_resume_metadata(resume_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get resume metadata from Firestore.

    Args:
        resume_id: Unique resume identifier
        user_id: User ID (for proper path lookup)

    Returns:
        Resume metadata dictionary or None if not found

    Example:
        metadata = get_resume_metadata("res123", "user123")
        if metadata:
            print(f"Resume: {metadata['originalFileName']}")
    """

    try:
        db = get_firestore_client()
        doc_ref = db.collection("users").document(user_id).collection("resumes").document(resume_id)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        return None

    except Exception as e:
        raise Exception(f"Failed to get resume metadata: {str(e)}")


def list_user_resumes(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    List all resumes for a specific user.

    Args:
        user_id: Firebase Auth user ID
        limit: Maximum number of resumes to return (default: 50)

    Returns:
        List of resume metadata dictionaries, sorted by upload date (newest first)

    Example:
        resumes = list_user_resumes("user123")
        for resume in resumes:
            print(f"Resume: {resume['resumeId']}, uploaded: {resume['uploadedAt']}")
    """

    try:
        db = get_firestore_client()

        # Query user's resumes subcollection
        resumes_ref = (
            db.collection("users")
            .document(user_id)
            .collection("resumes")
            .order_by("uploadedAt", direction=firestore.Query.DESCENDING)
            .limit(limit)
        )

        docs = resumes_ref.stream()

        resumes = []
        for doc in docs:
            resume_data = doc.to_dict()
            resumes.append(resume_data)

        return resumes

    except Exception as e:
        raise Exception(f"Failed to list user resumes: {str(e)}")


def delete_resume_metadata(resume_id: str, user_id: str) -> None:
    """
    Delete resume metadata from Firestore.

    Args:
        resume_id: Unique resume identifier
        user_id: User ID (for authorization check)

    Note: This only deletes metadata. You should also delete files from Cloud Storage.
    """

    try:
        db = get_firestore_client()

        # Verify ownership before deleting
        metadata = get_resume_metadata(resume_id)
        if not metadata or metadata.get("userId") != user_id:
            raise Exception("Unauthorized: Resume not found or doesn't belong to user")

        # Delete from main resumes collection
        db.collection("resumes").document(resume_id).delete()

        # Delete from user's subcollection
        db.collection("users").document(user_id).collection("resumes").document(resume_id).delete()

    except Exception as e:
        raise Exception(f"Failed to delete resume metadata: {str(e)}")


def update_resume_status(resume_id: str, status: str) -> None:
    """
    Update resume processing status.

    Args:
        resume_id: Unique resume identifier
        status: New status (e.g., "uploaded", "processing", "optimized", "failed")

    Example:
        update_resume_status("res123", "processing")
        # ... process resume ...
        update_resume_status("res123", "optimized")
    """

    try:
        db = get_firestore_client()
        doc_ref = db.collection("resumes").document(resume_id)

        doc_ref.update({
            "status": status,
            "updatedAt": datetime.utcnow().isoformat()
        })

    except Exception as e:
        raise Exception(f"Failed to update resume status: {str(e)}")


def get_user_stats(user_id: str) -> Dict[str, Any]:
    """
    Get statistics for a user's resumes.

    Args:
        user_id: Firebase Auth user ID

    Returns:
        Dictionary with:
            - total_resumes: Total number of resumes uploaded
            - optimized_resumes: Number of resumes optimized
            - average_score: Average relevance score

    Example:
        stats = get_user_stats("user123")
        print(f"Total resumes: {stats['total_resumes']}")
    """

    try:
        resumes = list_user_resumes(user_id, limit=1000)

        total = len(resumes)
        optimized = sum(1 for r in resumes if r.get("status") == "optimized")

        scores = [r.get("relevanceScore", 0) for r in resumes if r.get("relevanceScore")]
        avg_score = sum(scores) / len(scores) if scores else 0

        return {
            "total_resumes": total,
            "optimized_resumes": optimized,
            "average_score": round(avg_score, 2),
            "recent_uploads": resumes[:5]  # 5 most recent
        }

    except Exception as e:
        raise Exception(f"Failed to get user stats: {str(e)}")


def create_user_document(user_id: str, email: str, display_name: Optional[str] = None) -> None:
    """
    Create user document in Firestore (called on first login).

    Args:
        user_id: Firebase Auth user ID
        email: User email
        display_name: User's display name (optional)

    Example:
        create_user_document("user123", "user@example.com", "John Doe")
    """

    try:
        db = get_firestore_client()

        user_ref = db.collection("users").document(user_id)

        # Only create if doesn't exist
        if not user_ref.get().exists:
            user_ref.set({
                "userId": user_id,
                "email": email,
                "displayName": display_name,
                "createdAt": datetime.utcnow().isoformat(),
                "lastLoginAt": datetime.utcnow().isoformat()
            })
        else:
            # Update last login
            user_ref.update({
                "lastLoginAt": datetime.utcnow().isoformat()
            })

    except Exception as e:
        raise Exception(f"Failed to create user document: {str(e)}")

"""
Google Cloud Storage Module

Handles file uploads and downloads to/from Google Cloud Storage.
For local testing, uses filesystem storage instead.
"""

import os
from typing import Optional
from pathlib import Path

# Check if we're in local testing mode
LOCAL_TESTING = os.getenv("LOCAL_TESTING", "false").lower() == "true"

# Local storage directory for testing
LOCAL_STORAGE_DIR = Path("/tmp/resumax-local-storage")

if LOCAL_TESTING:
    LOCAL_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Using local storage: {LOCAL_STORAGE_DIR}")
else:
    from google.cloud import storage


def get_storage_client():
    """
    Get Google Cloud Storage client.

    The client automatically uses credentials from:
        - Cloud Run environment (default service account)
        - GOOGLE_APPLICATION_CREDENTIALS environment variable
        - gcloud auth application-default login
    """
    if LOCAL_TESTING:
        return None  # Not needed for local storage
    return storage.Client()


def upload_to_gcs(
    bucket_name: str,
    destination_path: str,
    content: bytes,
    content_type: Optional[str] = None
) -> str:
    """
    Upload file content to Google Cloud Storage (or local filesystem in testing).

    Args:
        bucket_name: GCS bucket name (e.g., "resumax-resumes")
        destination_path: Path in bucket (e.g., "resumes/user123/original/resume.pdf")
        content: File content as bytes
        content_type: MIME type (e.g., "application/pdf")

    Returns:
        Public URL to the uploaded file

    Example:
        url = upload_to_gcs(
            bucket_name="resumax-resumes",
            destination_path="resumes/user123/original/resume.pdf",
            content=pdf_bytes,
            content_type="application/pdf"
        )
    """

    try:
        # LOCAL TESTING: Use filesystem
        if LOCAL_TESTING:
            local_path = LOCAL_STORAGE_DIR / destination_path
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(content)
            return f"local://{destination_path}"

        # PRODUCTION: Use GCS
        client = get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_path)

        # Set content type if provided
        if content_type:
            blob.content_type = content_type

        # Upload the file
        blob.upload_from_string(content)

        # Return the public URL
        return f"gs://{bucket_name}/{destination_path}"

    except Exception as e:
        raise Exception(f"Failed to upload to GCS: {str(e)}")


def download_from_gcs(bucket_name: str, source_path: str) -> bytes:
    """
    Download file from Google Cloud Storage (or local filesystem in testing).

    Args:
        bucket_name: GCS bucket name
        source_path: Path in bucket

    Returns:
        File content as bytes

    Example:
        content = download_from_gcs(
            bucket_name="resumax-resumes",
            source_path="resumes/user123/original/resume.pdf"
        )
    """

    try:
        # LOCAL TESTING: Use filesystem
        if LOCAL_TESTING:
            local_path = LOCAL_STORAGE_DIR / source_path
            if not local_path.exists():
                raise FileNotFoundError(f"File not found: {source_path}")
            return local_path.read_bytes()

        # PRODUCTION: Use GCS
        client = get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(source_path)

        # Download as bytes
        content = blob.download_as_bytes()
        return content

    except Exception as e:
        raise Exception(f"Failed to download from GCS: {str(e)}")


def delete_from_gcs(bucket_name: str, path: str) -> None:
    """
    Delete a file from Google Cloud Storage.

    Args:
        bucket_name: GCS bucket name
        path: Path in bucket to delete

    Example:
        delete_from_gcs(
            bucket_name="resumax-resumes",
            path="resumes/user123/original/resume.pdf"
        )
    """

    try:
        # LOCAL TESTING: Delete from filesystem
        if LOCAL_TESTING:
            local_path = LOCAL_STORAGE_DIR / path
            if local_path.exists():
                local_path.unlink()
            return

        # PRODUCTION: Delete from GCS
        client = get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(path)
        blob.delete()

    except Exception as e:
        raise Exception(f"Failed to delete from GCS: {str(e)}")


def generate_signed_url(
    bucket_name: str,
    path: str,
    expiration_minutes: int = 60
) -> str:
    """
    Generate a signed URL for secure file access.

    Signed URLs allow temporary access to private files without authentication.

    Args:
        bucket_name: GCS bucket name
        path: Path in bucket
        expiration_minutes: How long the URL should be valid (default: 60 minutes)

    Returns:
        Signed URL string

    Example:
        url = generate_signed_url(
            bucket_name="resumax-resumes",
            path="resumes/user123/optimized/resume.pdf",
            expiration_minutes=30
        )
        # User can download from this URL for next 30 minutes
    """

    from datetime import timedelta

    try:
        client = get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(path)

        # Generate signed URL
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=expiration_minutes),
            method="GET"
        )

        return url

    except Exception as e:
        raise Exception(f"Failed to generate signed URL: {str(e)}")


def list_files(bucket_name: str, prefix: str) -> list:
    """
    List files in a bucket with a given prefix.

    Args:
        bucket_name: GCS bucket name
        prefix: Path prefix (e.g., "resumes/user123/")

    Returns:
        List of file paths

    Example:
        files = list_files(
            bucket_name="resumax-resumes",
            prefix="resumes/user123/"
        )
        # Returns: ["resumes/user123/original/resume.pdf", ...]
    """

    try:
        client = get_storage_client()
        bucket = client.bucket(bucket_name)

        # List blobs with prefix
        blobs = bucket.list_blobs(prefix=prefix)

        return [blob.name for blob in blobs]

    except Exception as e:
        raise Exception(f"Failed to list files: {str(e)}")


def create_bucket_if_not_exists(bucket_name: str, location: str = "us-central1") -> None:
    """
    Create a GCS bucket if it doesn't already exist.

    Args:
        bucket_name: Name for the bucket
        location: GCS region (default: us-central1)

    Note: This requires proper permissions. In production, buckets should be
    created manually or via Terraform.
    """

    try:
        client = get_storage_client()

        # Check if bucket exists
        bucket = client.bucket(bucket_name)
        if bucket.exists():
            print(f"Bucket {bucket_name} already exists")
            return

        # Create bucket
        bucket = client.create_bucket(bucket_name, location=location)
        print(f"Created bucket {bucket_name} in {location}")

    except Exception as e:
        print(f"Failed to create bucket: {str(e)}")

"""
Google Cloud Storage Module

Handles file uploads and downloads to/from Google Cloud Storage.
"""

import os
from typing import Optional
from google.cloud import storage


def get_storage_client():
    """
    Get Google Cloud Storage client.

    The client automatically uses credentials from:
        - Cloud Run environment (default service account)
        - GOOGLE_APPLICATION_CREDENTIALS environment variable
        - gcloud auth application-default login
    """
    return storage.Client()


def upload_to_gcs(
    bucket_name: str,
    destination_path: str,
    content: bytes,
    content_type: Optional[str] = None
) -> str:
    """
    Upload file content to Google Cloud Storage.

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
        client = get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_path)

        # Set content type if provided
        if content_type:
            blob.content_type = content_type

        # Upload the file
        blob.upload_from_string(content)

        # Make the file publicly readable (optional - you may want signed URLs instead)
        # blob.make_public()

        # Return the public URL
        return f"gs://{bucket_name}/{destination_path}"

    except Exception as e:
        raise Exception(f"Failed to upload to GCS: {str(e)}")


def download_from_gcs(bucket_name: str, source_path: str) -> bytes:
    """
    Download file from Google Cloud Storage.

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

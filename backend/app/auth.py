import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Initialize Firebase Admin
# In Cloud Run, it auto-detects credentials. Locally, it needs GOOGLE_APPLICATION_CREDENTIALS env var.
if not firebase_admin._apps:
    try:
        firebase_admin.initialize_app()
        print("✅ Firebase Admin initialized")
    except Exception as e:
        print(f"⚠️ Failed to initialize Firebase Admin: {e}")
        print("Auth verification might fail if credentials are not set up.")

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verify Firebase ID token and return user_id.
    """
    token = credentials.credentials
    try:
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['uid']
        return user_id
    except Exception as e:
        print(f"Auth Error: {e}")
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_optional_user(credentials: HTTPAuthorizationCredentials = Security(security_optional)) -> str:
    """
    Optional auth for endpoints that might work without it (or for testing).
    Returns user_id if valid, else None.
    """
    if not credentials:
        return None
        
    try:
        return get_current_user(credentials)
    except:
        return None

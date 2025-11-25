import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# LOCAL TESTING MODE - Set LOCAL_TESTING=true to skip Firebase auth
LOCAL_TESTING = os.getenv("LOCAL_TESTING", "false").lower() == "true"

# Initialize Firebase Admin
# In Cloud Run, it auto-detects credentials. Locally, it needs GOOGLE_APPLICATION_CREDENTIALS env var.
if not LOCAL_TESTING and not firebase_admin._apps:
    try:
        firebase_admin.initialize_app()
        print("✅ Firebase Admin initialized")
    except Exception as e:
        print(f"⚠️ Failed to initialize Firebase Admin: {e}")
        print("   Set LOCAL_TESTING=true to skip auth for testing")

if LOCAL_TESTING:
    print("⚠️  LOCAL_TESTING mode enabled - auth will be bypassed!")

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verify Firebase ID token and return user_id.
    In LOCAL_TESTING mode, accepts any token and returns test-user-123
    """
    # LOCAL TESTING MODE - bypass auth
    if LOCAL_TESTING:
        return "test-user-123"

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

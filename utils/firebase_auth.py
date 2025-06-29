import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

# Init Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "token_uri": "https://oauth2.googleapis.com/token"
    })
    firebase_admin.initialize_app(cred)


def verify_firebase_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth header")

    token = auth_header.split("Bearer ")[-1]
    try:
        decoded_token = auth.verify_id_token(token)
        request.state.user_id = decoded_token["uid"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")


def get_user_id(request: Request):
    return getattr(request.state, "user_id", None)

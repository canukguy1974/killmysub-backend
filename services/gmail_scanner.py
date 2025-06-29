import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from base64 import urlsafe_b64decode
import re
from datetime import datetime

def scan_gmail_for_subscriptions(user_id):
    creds = Credentials(
        None,
        refresh_token=os.getenv("GMAIL_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GMAIL_CLIENT_ID"),
        client_secret=os.getenv("GMAIL_CLIENT_SECRET"),
    )

    service = build("gmail", "v1", credentials=creds)
    result = service.users().messages().list(userId="me", q="unsubscribe", maxResults=20).execute()
    messages = result.get("messages", [])

    subscriptions = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_detail.get("payload", {}).get("headers", [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        from_email = next((h['value'] for h in headers if h['name'] == 'From'), '(No Sender)')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), '')

        subscriptions.append({
            "user_id": user_id,
            "service": from_email,
            "subject": subject,
            "date": date,
            "timestamp": datetime.utcnow().isoformat()
        })

    return subscriptions

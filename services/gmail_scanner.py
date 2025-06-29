import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def scan_gmail_for_subscriptions(user_id: str):
    creds = Credentials(
        None,
        refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"),
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token"
    )

    # Refresh access token
    creds.refresh(Request())

    # Build Gmail service
    service = build("gmail", "v1", credentials=creds)

    # Search for unsubscribe emails
    result = service.users().messages().list(userId="me", q="unsubscribe", maxResults=20).execute()
    messages = result.get("messages", [])

    subs = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "")
        subs.append({"subject": subject, "from": sender})

    return subs

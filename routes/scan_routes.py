from fastapi import APIRouter, Request
from services.gmail_scanner import scan_gmail_for_subscriptions
from services.sms_alert import send_sms_alert
from utils.firebase_auth import get_user_id
from pymongo import MongoClient
import os

router = APIRouter()

# Mongo setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["killmysub"]
subs_collection = db["subscriptions"]

@router.post("/now")
async def scan_now(request: Request):
    user_id = "testuser@example.com"
    subs = scan_gmail_for_subscriptions(user_id)
    
    # Store in DB
    for sub in subs:
        subs_collection.update_one(
            {"user_id": user_id, "service": sub["service"]},
            {"$set": sub},
            upsert=True
        )

    # Send SMS
    send_sms_alert(user_id, subs)
    return {"message": "Scan complete", "found": len(subs)}


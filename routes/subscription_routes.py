from fastapi import APIRouter, Request
from pymongo import MongoClient
import os
from utils.firebase_auth import get_user_id

router = APIRouter()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["killmysub"]
subs_collection = db["subscriptions"]

@router.get("/")
async def get_subscriptions(request: Request):
    user_id = get_user_id(request)
    subs = list(subs_collection.find({"user_id": user_id}, {"_id": 0}))
    return {"subscriptions": subs}

@router.post("/unsubscribe")
async def unsubscribe(request: Request):
    user_id = get_user_id(request)
    data = await request.json()
    service = data.get("service")

    if service:
        subs_collection.delete_one({"user_id": user_id, "service": service})
        return {"message": f"Unsubscribed from {service}"}
    return {"error": "Missing service name"}

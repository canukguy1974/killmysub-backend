import os
from twilio.rest import Client
from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient(os.getenv("MONGO_URI"))
db = client["killmysub"]
users = db["users"]


def send_sms_alert(user_id, subs):
    if not subs:
        return

    twilio_client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
    user = users.find_one({"_id": user_id})

    # Prevent SMS spam
    last_sent = user.get("last_alert_sent") if user else None
    if last_sent:
        last_time = datetime.fromisoformat(last_sent)
        if datetime.utcnow() - last_time < timedelta(hours=24):
            print("SMS recently sent — skipping.")
            return

    body = f"KillMySub found {len(subs)} subscriptions in your inbox. Time to cancel? 💸"
    if user and "phone" in user:
        twilio_client.messages.create(
            body=body,
            from_=os.getenv("TWILIO_NUMBER"),
            to=user["phone"]
        )
        users.update_one({"_id": user_id}, {"$set": {"last_alert_sent": datetime.utcnow().isoformat()}})

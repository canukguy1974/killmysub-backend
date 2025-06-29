from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from routes.scan_routes import router as scan_router
from routes.subscription_routes import router as subscription_router
from utils.firebase_auth import verify_firebase_token

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/ping")
def ping():
    return {"message": "pong"}


# Routes
app.include_router(scan_router, prefix="/scan", dependencies=[Depends(verify_firebase_token)])
app.include_router(subscription_router, prefix="/subscriptions", dependencies=[Depends(verify_firebase_token)])

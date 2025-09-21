import os
from datetime import datetime

USE_FIRESTORE = os.getenv("USE_FIRESTORE", "false").lower() == "true"

if USE_FIRESTORE:
    from google.cloud import firestore
    db = firestore.Client()
    COLLECTION = os.getenv("FIRESTORE_COLLECTION", "wellness_logs")

def save_log_optional(session_id: str, mood: str, user_input: str, ai_reply: str, crisis: bool, screened: str):
    if not USE_FIRESTORE:
        return
    doc = {
        "session_id": session_id,
        "ts": datetime.utcnow().isoformat(),
        "mood": mood,
        "user_input": user_input[:1000],
        "ai_reply": ai_reply[:2000],
        "crisis": crisis,
        "screened": screened,
    }
    db.collection(os.getenv("FIRESTORE_COLLECTION", "wellness_logs")).add(doc)

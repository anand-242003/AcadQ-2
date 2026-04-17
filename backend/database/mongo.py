import os
from datetime import datetime
from pymongo import MongoClient, ASCENDING
from pymongo.database import Database
from dotenv import load_dotenv

load_dotenv()

_client: MongoClient | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        _client = MongoClient(
            mongo_uri,
            tlsAllowInvalidCertificates=True,
        )
    return _client


def get_db() -> Database:
    client = get_client()
    db = client["acadiq"]
    # Ensure unique index on email
    db["users"].create_index([("email", ASCENDING)], unique=True)
    return db


def find_user_by_email(email: str) -> dict | None:
    db = get_db()
    return db["users"].find_one({"email": email})


def insert_user(user: dict) -> str:
    db = get_db()
    result = db["users"].insert_one(user)
    return str(result.inserted_id)


def user_exists(email: str) -> bool:
    db = get_db()
    return db["users"].count_documents({"email": email}) > 0


# ─── Reports ──────────────────────────────────────────────────────────────────

def insert_report(report: dict) -> str:
    db = get_db()
    result = db["reports"].insert_one(report)
    return str(result.inserted_id)


def get_reports_by_user(email: str) -> list[dict]:
    db = get_db()
    return list(db["reports"].find({"user_email": email}).sort("timestamp", -1))

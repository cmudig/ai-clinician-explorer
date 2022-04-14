from firebase_admin import credentials, firestore, initialize_app
import os

FIRESTORE_KEY_PATH = os.environ.get("FIRESTORE_KEY_PATH") or "firestore_key.json"

# Initialize Firestore DB
cred = credentials.Certificate(FIRESTORE_KEY_PATH)
default_app = initialize_app(cred)
db = firestore.client()
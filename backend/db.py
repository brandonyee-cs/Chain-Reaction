import firebase_admin
from firebase_admin import credentials, firestore
import json

# Load Firebase credentials from the key.json file
with open('c:/Users/Fezan/Downloads/hackknight/hackknight/backend/key.json') as f:
    key = json.load(f)

cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()

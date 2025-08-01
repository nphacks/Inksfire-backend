import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('firebase-v2-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
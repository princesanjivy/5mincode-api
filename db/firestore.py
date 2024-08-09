from firebase_admin import credentials
from firebase_admin import firestore as admin
from firebase_admin import initialize_app
from google.cloud import firestore


# Singleton class
class FirebaseFirestore:
    _instance = None
    instance: firestore.Client  # Type hint for autocompletion

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseFirestore, cls).__new__(cls)
            # Initialize the Firebase app only once
            creds = credentials.Certificate("saKey.json")
            initialize_app(creds)
            cls._instance.instance = admin.client()
        return cls._instance

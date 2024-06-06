import firebase_admin
from firebase_admin import credentials, firestore
import os

# Path to your service account key JSON file
service_account_path = '/home/aetooc/crewai/jaaoo-9s6hwv-firebase-adminsdk-shxwd-bf5a7f7437.json'

# Check if the service account file exists
if not os.path.exists(service_account_path):
    raise FileNotFoundError(f"Service account key file not found: {service_account_path}")

# Initialize the Firebase app with the service account
try:
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)
except ValueError as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    exit(1)

# Initialize Firestore
db = firestore.client()

# Retrieve specific fields from a Firestore document using its document ID  
def get_document_fields(collection_name, document_id):
    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"No document found with ID: {document_id}")
            return None
    except Exception as e:
        print(f"Error retrieving document from Firestore: {e}")
        return None



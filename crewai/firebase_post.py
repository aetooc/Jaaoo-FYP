import os
import firebase_admin
from firebase_admin import credentials, firestore

# Path to your service account key file
service_account_path = '/home/aetooc/crewai/jaaoo-9s6hwv-firebase-adminsdk-shxwd-bf5a7f7437.json'

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

# Upload data to a Firestore document
def upload_document(collection_name, document_id, data):
    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.set(data)
        print(f"Document successfully written with ID: {document_id}")
    except Exception as e:
        print(f"Error writing document to Firestore: {e}")

# Example usage
if __name__ == "__main__":
    # Retrieve a document
    # collection_name = 'Data'
    # # Upload a document
    # new_document_id = '1957578357457'
    # new_document_data = {
    #     'Plan': 'value1',
    #     'Airbnb': 'value2',
    #     'field3': 'value3'
    # }
    # new_document_data.update({field: value})

    upload_document(collection_name, new_document_id, new_document_data)

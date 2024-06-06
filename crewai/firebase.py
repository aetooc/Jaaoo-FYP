import os
from google.cloud import firestore

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "jaaoo-app-a7509eaeb341.json"


db = firestore.Client()



user_id = "vhv2rFVDwXegnWHuRCQolCZqHJJ3"
user_ref = db.collection('User').document(user_id)
user_doc = user_ref.get()

if user_doc.exists:
    print(f'User Data: {user_doc.to_dict()}')
else:
    print('No such user found')
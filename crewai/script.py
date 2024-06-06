# Define the file name
file_name = 'output.txt'

# import os
# from google.cloud import firestore

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "jaaoo-app-a7509eaeb341.json"


# db = firestore.Client()



# user_id = "vhv2rFVDwXegnWHuRCQolCZqHJJ3"
# user_ref = db.collection('User').document(user_id)
# user_doc = user_ref.get()

# Open the file for reading
with open(file_name, 'r') as file:
    # Read the entire content of the file
    file_content = file.read()
    
    # Print the content
    print(file_content)
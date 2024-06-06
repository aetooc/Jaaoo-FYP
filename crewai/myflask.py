from flask import Flask, jsonify
import os
from google.cloud import firestore
import subprocess



# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "jaaoo-app-a7509eaeb341.json"

# db = firestore.Client()



app = Flask(__name__)

@app.route('/run-script', methods=['GET'])
def run_script():
    # Replace 'your_script.py' with the path to your Python script
    result = subprocess.run(['python', 'script.py'], capture_output=True, text=True)
    output = result.stdout
    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(debug=True ,  host='0.0.0.0')
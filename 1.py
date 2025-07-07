from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("service_account.json")
initialize_app(cred)

db = firestore.client()

# Test data
user_id = "test_user"
project_name = "Test_Project"
data = {
    "title": "Test Project",
    "created_at": datetime.now().strftime('%Y-%m-%d %H:%M'),
    "status": "completed"
}

# Save to Firestore
db.collection('users').document(user_id).collection('projects').document(project_name).set(data)

print("✅ Data saved successfully.")

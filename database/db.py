import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/PC-16/Desktop/reel_invitation_creator/service_account.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✔️ Load Projects
def load_projects(user_id):
    projects_ref = db.collection('users').document(user_id).collection('projects')
    docs = projects_ref.stream()
    return {doc.id: doc.to_dict() for doc in docs}

# ✔️ Save Project
def save_project(user_id, name, data):
    data["last_modified"] = datetime.now().strftime('%Y-%m-%d %H:%M')
    if "status" not in data:
        data["status"] = "ongoing"
    db.collection('users').document(user_id).collection('projects').document(name).set(data)

# ✔️ Delete Project
def delete_project(user_id, name):
    db.collection('users').document(user_id).collection('projects').document(name).delete()

# ✔️ Duplicate Project
def duplicate_project(user_id, name):
    projects = load_projects(user_id)
    if name in projects:
        new_name = f"{name}_copy"
        counter = 1
        while new_name in projects:
            new_name = f"{name}_copy_{counter}"
            counter += 1

        new_data = projects[name].copy()
        new_data["last_modified"] = datetime.now().strftime('%Y-%m-%d %H:%M')

        db.collection('users').document(user_id).collection('projects').document(new_name).set(new_data)

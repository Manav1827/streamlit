# import firebase_admin
# from firebase_admin import credentials, firestore
# from datetime import datetime

# # Initialize Firebase
# if not firebase_admin._apps:
#     cred = credentials.Certificate("C:/Users/PC-16/Desktop/reel_invitation_creator/service_account.json")
#     firebase_admin.initialize_app(cred)

# db = firestore.client()

# # ✔️ Create Project
# def save_project(user_id, name, data):
#     data["last_modified"] = datetime.now().strftime('%Y-%m-%d %H:%M')
#     if "status" not in data:
#         data["status"] = "ongoing"
#     db.collection('users').document(user_id).collection('projects').document(name).set(data)

# # ✔️ Read Projects
# def read_projects(user_id):
#     return db.collection('users').document(user_id).collection('projects').stream()

# # ✔️ Delete
# def delete_project(user_id, name):
#     db.collection('users').document(user_id).collection('projects').document(name).delete()

# # ✔️ Update
# def update_project(user_id, name, data):
#     db.collection('users').document(user_id).collection('projects').document(name).update(data)

# # ✔️ Duplicate
# def duplicate_project(user_id, name):
#     projects = {doc.id: doc.to_dict() for doc in read_projects(user_id)}
#     if name in projects:
#         new_name = f"{name}_copy"
#         counter = 1
#         while new_name in projects:
#             new_name = f"{name}_copy_{counter}"
#             counter += 1

#         new_data = projects[name].copy()
#         new_data["last_modified"] = datetime.now().strftime('%Y-%m-%d %H:%M')

#         db.collection('users').document(user_id).collection('projects').document(new_name).set(new_data)

#2 working
# import firebase_admin
# from firebase_admin import credentials, firestore
# from datetime import datetime
# import re

# # Initialize Firebase
# if not firebase_admin._apps:
#     cred = credentials.Certificate("C:/Users/PC-16/Desktop/reel_invitation_creator/service_account.json")
#     firebase_admin.initialize_app(cred)

# db = firestore.client()

# def sanitize_id(text):
#     return re.sub(r'[^a-zA-Z0-9_]+', '_', text).strip("_")

# # ✔️ Create or Overwrite Project
# def save_project(user_id, name, data):
#     data["last_modified"] = datetime.now().strftime('%Y-%m-%d %H:%M')
#     data.setdefault("status", "ongoing")
#     project_id = sanitize_id(name)
#     db.collection('users').document(user_id).collection('projects').document(project_id).set(data)

# # ✔️ Read All Projects (sorted by modified time)
# def read_projects(user_id):
#     return db.collection('users').document(user_id).collection('projects')\
#              .order_by("last_modified", direction=firestore.Query.DESCENDING).stream()

# # ✔️ Optional: Return as dict
# def read_projects_dict(user_id):
#     return {doc.id: doc.to_dict() for doc in read_projects(user_id)}

# # ✔️ Delete Project
# def delete_project(user_id, name):
#     project_id = sanitize_id(name)
#     db.collection('users').document(user_id).collection('projects').document(project_id).delete()

# # ✔️ Update Project
# def update_project(user_id, name, data):
#     project_id = sanitize_id(name)
#     db.collection('users').document(user_id).collection('projects').document(project_id).update(data)

# # ✔️ Duplicate Project
# def duplicate_project(user_id, name):
#     projects = read_projects_dict(user_id)
#     if name in projects:
#         new_name = f"{name}_copy"
#         counter = 1
#         while sanitize_id(new_name) in projects:
#             new_name = f"{name}_copy_{counter}"
#             counter += 1

#         new_data = projects[name].copy()
#         new_data["last_modified"] = datetime.now().strftime('%Y-%m-%d %H:%M')

#         db.collection('users').document(user_id).collection('projects')\
#             .document(sanitize_id(new_name)).set(new_data)

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import re

# 🔐 Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/PC-16/Desktop/reel_invitation_creator/service_account.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 🧼 Sanitize for Firestore document ID
def sanitize_id(text):
    return re.sub(r'[^a-zA-Z0-9_]+', '_', text).strip("_")

# ✔️ Save or Overwrite Project
def save_project(user_id, name, data):
    data["last_modified"] = datetime.now().strftime('%Y-%m-%d %H:%M')
    data.setdefault("status", "ongoing")
    project_id = sanitize_id(name)
    db.collection('users').document(user_id).collection('projects').document(project_id).set(data)

# ✔️ Read All Projects (sorted by last modified)
def read_projects(user_id):
    return db.collection('users').document(user_id).collection('projects')\
             .order_by("last_modified", direction=firestore.Query.DESCENDING).stream()

# ✔️ Read Projects as Dictionary
def read_projects_dict(user_id):
    return {doc.id: doc.to_dict() for doc in read_projects(user_id)}

# ✔️ Delete Project
def delete_project(user_id, name_or_id):
    project_id = sanitize_id(name_or_id)
    db.collection('users').document(user_id).collection('projects').document(project_id).delete()

# ✔️ Update Project Fields
def update_project(user_id, name_or_id, data):
    project_id = sanitize_id(name_or_id)
    data["last_modified"] = datetime.now().strftime('%Y-%m-%d %H:%M')
    db.collection('users').document(user_id).collection('projects').document(project_id).update(data)

# ✔️ Duplicate Project
def duplicate_project(user_id, name_or_id):
    projects = read_projects_dict(user_id)
    base_id = sanitize_id(name_or_id)

    if base_id in projects:
        original = projects[base_id]
        new_name = f"{original['title']}_copy"
        counter = 1

        while sanitize_id(new_name) in projects:
            new_name = f"{original['title']}_copy_{counter}"
            counter += 1

        new_data = original.copy()
        new_data["title"] = new_name
        new_data["created_at"] = datetime.now().strftime('%Y-%m-%d %H:%M')
        new_data["last_modified"] = new_data["created_at"]
        new_data["status"] = "ongoing"

        db.collection('users').document(user_id).collection('projects')\
            .document(sanitize_id(new_name)).set(new_data)

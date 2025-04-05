from flask import Blueprint, request, jsonify
from pymongo import MongoClient

auth_bp = Blueprint('auth', __name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['employee_db']
users = db.users

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if users.find_one({"$or": [{"email": email}, {"name": name}]}):
        return jsonify({"message": "User already exists"}), 400

    users.insert_one({
        "name": name,
        "email": email,
        "password": password  # ⚠️ In production, hash passwords!
    })

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('email')  # Can be name or email
    password = data.get('password')

    user = users.find_one({
        "$or": [{"email": identifier}, {"name": identifier}],
        "password": password
    })

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

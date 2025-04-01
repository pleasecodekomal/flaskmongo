from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Database Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['employee_db']
users_collection = db['users']

# REGISTER Route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # Check if user already exists
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({"username": username, "password": hashed_password})

    return jsonify({"message": "User registered successfully"}), 201


# LOGIN Route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({"username": username})
    
    if user and check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

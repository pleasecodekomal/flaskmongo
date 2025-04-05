from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
from routes.employee_routes import employee_bp
from routes.auth_routes import auth_bp
from data_preprocessing.interpretation import analyze_employee_data
from data_preprocessing.preprocessing import clean_employee_data
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# ========== Database ==========
client = MongoClient('mongodb://localhost:27017/')
db = client['employee_db']

# ========== Page Routes ==========
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add-employee')
def add_employee():
    if 'user' not in session:
        return redirect(url_for('landing'))  # Redirect to login page
    return render_template('add_employee.html')

@app.route('/view-employees')
def view_employees():
    return render_template('view_employees.html')

# ========== API Routes ==========
@app.route('/api/employee/preprocess', methods=['POST'])
def preprocess_employee_data():
    data = request.json  # Expecting JSON input
    cleaned_data = clean_employee_data(data)
    return jsonify({"cleaned_data": cleaned_data.to_dict(orient="records")})

@app.route('/api/employee/analyze', methods=['GET'])
def analyze_employee_data_route():
    employees = list(db.employees.find({}, {"_id": 0}))  # Fetch data from MongoDB
    df = pd.DataFrame(employees)
    insights = analyze_employee_data(df)
    return jsonify(insights)

# ========== Auth Session API ==========
@app.route('/session-login', methods=['POST'])
def session_login():
    data = request.json
    identifier = data.get('email')
    password = data.get('password')
    user = db.users.find_one({
        "$or": [{"email": identifier}, {"name": identifier}],
        "password": password
    })
    if user:
        session['user'] = user['name']
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('landing'))

# ========== Register Blueprints ==========
app.register_blueprint(employee_bp, url_prefix="/api/employee")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == '__main__':
    app.run(debug=True)

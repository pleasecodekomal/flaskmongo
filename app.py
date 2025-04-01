from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from routes.employee_routes import employee_bp
from routes.auth_routes import auth_bp
from data_preprocessing.interpretation import analyze_employee_data
from data_preprocessing.preprocessing import clean_employee_data
import pandas as pd
app = Flask(__name__)

# Database Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['employee_db']

@app.route('/')
def index():
    return render_template('index.html')

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

# Register Blueprints
app.register_blueprint(employee_bp, url_prefix="/api/employee")
app.register_blueprint(auth_bp, url_prefix="/auth") 

if __name__ == '__main__':
    app.run(debug=True)

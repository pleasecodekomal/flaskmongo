from flask import Flask,render_template,jsonify
from pymongo import MongoClient
from routes.employee_routes import employee_bp
from routes.auth_routes import auth_bp  # Import the auth routes

app = Flask(__name__)

# Database Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['employee_db']

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')
# Register Blueprints
app.register_blueprint(employee_bp, url_prefix="/api/employee")
app.register_blueprint(auth_bp, url_prefix="/auth") 

if __name__ == '__main__':
    app.run(debug=True)

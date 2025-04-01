from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db['employees']

def format_employee(employee):
    employee['_id'] = str(employee['_id'])
    return employee

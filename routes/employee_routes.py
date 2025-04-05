from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from models.employee import collection, format_employee

employee_bp = Blueprint("employee", __name__)

# GET - Fetch Employees
@employee_bp.route("/", methods=["GET"])
def get_employee():
    empid = request.args.get("empid")
    if empid:
        employee = collection.find_one({"empid": int(empid)})
        if employee:
            return jsonify(format_employee(employee)), 200
        return jsonify({"error": "No employee found"}), 404
    else:
        employees = list(collection.find())
        return jsonify([format_employee(emp) for emp in employees]), 200

# POST - Add Employees
@employee_bp.route("/", methods=["POST"])
def add_employees():
    data = request.json
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    return jsonify({"message": "Employee details inserted"}), 201

# PUT - Update Employee by _id
@employee_bp.route("/<id>", methods=["PUT"])
def update_employee(id):
    try:
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": request.json})
        if result.matched_count:
            return jsonify({"message": "Employee details updated"}), 200
        return jsonify({"error": "No employee found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# DELETE - Remove Employee by _id
@employee_bp.route("/<id>", methods=["DELETE"])
def delete_employee(id):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Employee deleted"}), 200
        return jsonify({"error": "No employee found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

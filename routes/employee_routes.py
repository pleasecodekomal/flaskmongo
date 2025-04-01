from flask import Blueprint, request, jsonify
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

# PUT - Update Employee
@employee_bp.route("/", methods=["PUT"])
def update_employee():
    empid = request.json.get("empid")
    if empid:
        result = collection.update_one({"empid": int(empid)}, {"$set": request.json})
        if result.matched_count:
            return jsonify({"message": "Employee details updated"}), 200
        return jsonify({"error": "No employee found"}), 404
    return jsonify({"error": "Provide an empid to update the details"}), 400

# DELETE - Remove Employee
@employee_bp.route("/", methods=["DELETE"])
def delete_employee():
    empid = request.json.get("empid")
    if empid:
        result = collection.delete_one({"empid": int(empid)})
        if result.deleted_count:
            return jsonify({"message": "Employee deleted"}), 200
        return jsonify({"error": "No employee found"}), 404
    return jsonify({"error": "Provide an empid to delete the employee"}), 400

from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db =client['employee_db']
collection=db['employees']

def format_employee(employee):
    employee['_id'] =str(employee['_id'])
    return employee

#get method

@app.route('/api/employee' ,methods=['GET'])
def get_employee():
    empid=request.args.get('empid')
    if empid:
        employee=collection.find_one({'empid':int(empid)})
        if employee:
            return jsonify(format_employee(employee)),200
        return jsonify({'error':'No employee found'}),404
    else:
        employees=list(collection.find())
        return jsonify([format_employee(emp) for emp in employees]),200
    
@app.route('/api/employee',methods=['POST'])
def add_employees():
    data=request.json
    if isinstance(data,list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    return jsonify({'message':'Employee details inserted'}),201

@app.route('/api/employee',methods=['PUT'])
def update_employee():
    empid=request.json['empid']
    data=request.json

    if empid:
        result=collection.update_one({'empid':int(empid)},{'$set':data})
        if result.matched_count:
            return jsonify({'message':'Employee details updated'}),200
        return jsonify({'error':'No employee found'}),404
    return jsonify({'error':'Provide an empid to update the details'}),400



@app.route('/api/employee',methods=['DELETE'])
def delete_employee():
    empid=request.json['empid']
    if empid:
        result=collection.delete_one({'empid':int(empid)})
        if result.deleted_count:
            return jsonify({'message':'Employee deleted'}),200
        return jsonify({'error':'No employee found'}),404
    return jsonify({'message':'Provide an empid to update details'}),400

if __name__=='__main__':
    app.run(debug=True)

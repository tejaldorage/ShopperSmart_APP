from flask import Blueprint, request, jsonify
from database import sessionlocal
from models.customer import Customer

customer_n= Blueprint('customers', __name__)

@customer_n.route('/customers',methods=['POST'])
def add_customer():
    db=sessionlocal()
    data=request.json
    customer = Customer(name = data.get('name'),
                        email = data.get('email'),
                        phone_no = data.get('phone_no'),
                        location = data.get('location'))
    db.add(customer)
    db.commit()
    db.refresh(customer)
    db.close()
    return jsonify({"customer_id":customer.customer_id})

@customer_n.route('/customers',methods = ['GET'])
def get_all():
    db = sessionlocal()
    customers = db.query(Customer).all()
    db.close()
    return jsonify([
        {
            "customer_id":c.customer_id,
            "name":c.name,
            "email":c.email,
            "phone_no":c.phone_no,
            "location":c.location
        }for c in customers
    ])

@customer_n.route('/customers/<int:customer_id>',methods = ['GET'])
def get_by_id(customer_id):
    db=sessionlocal()
    customer = db.query(Customer).get(customer_id)
    db.close()
    if customer:
        return jsonify({
            "customer_id": customer.customer_id,
            "name": customer.name,
            "email": customer.email,
            "phone_no": customer.phone_no,
            "location":customer.location
        })
    return jsonify({"error": "Customer not found"}), 404

@customer_n.route('/customers/<int:customer_id>',methods=['PUT'])
def update(customer_id):
    db=sessionlocal()
    customer = db.query(Customer).get(customer_id)
    if not customer:
        db.close()
        return jsonify ({"error":"customer not found"}),404
    data = request.json
    data = request.json
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone_no = data.get('phone_no', customer.phone_no)
    customer.location = data.get('location',customer.location)

    db.commit()
    db.refresh(customer)
    db.close()
    return jsonify({
        "customer_id": customer.customer_id,
        "name": customer.name,
        "email": customer.email,
        "phone_no": customer.phone_no,
        "location": customer.location
    })

@customer_n.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    db = sessionlocal()
    customer = db.query(Customer).get(customer_id)
    if not customer:
        db.close()
        return jsonify({"error": "Customer not found"}), 404

    db.delete(customer)
    db.commit()
    db.close()
    return jsonify({"message": "Customer deleted"})    

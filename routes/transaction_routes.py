from flask import Blueprint, request, jsonify
from database import sessionlocal
from models.transaction import Transaction
from datetime import datetime

transaction_n = Blueprint('transactions', __name__)



@transaction_n.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    db = sessionlocal()


    purchase_date_str = data.get("purchase_date")
    if purchase_date_str:
        try:
            purchase_date = datetime.fromisoformat(purchase_date_str)
        except ValueError:
            return {"error": "Invalid datetime format. Use ISO format."}, 400
    else:
        purchase_date = None  

    transaction = Transaction(
        customer_id=data["customer_id"],
        product_id=data["product_id"],
        purchase_date=purchase_date  
    )

    db.add(transaction)
    db.commit()

    return {"message": "Transaction added successfully"}

@transaction_n.route('/transactions', methods=['GET'])
def get_all_transactions():
    db = sessionlocal()
    transactions = db.query(Transaction).all()
    db.close()
    return jsonify([
        {
            "transaction_id": t.transaction_id,
            "customer_id": t.customer_id,
            "product_id": t.product_id,
            "purchase_date": t.purchase_date.isoformat() if t.purchase_date else None
        } for t in transactions
    ])

@transaction_n.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction_by_id(transaction_id):
    db = sessionlocal()
    transaction = db.query(Transaction).get(transaction_id)
    db.close()
    if transaction:
        return jsonify({
            "transaction_id": transaction.transaction_id,
            "customer_id": transaction.customer_id,
            "product_id": transaction.product_id,
            "purchase_date": transaction.purchase_date.isoformat() if transaction.purchase_date else None
        })
    return jsonify({"error": "Transaction not found"}), 404

@transaction_n.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    db = sessionlocal()
    transaction = db.query(Transaction).get(transaction_id)
    if not transaction:
        db.close()
        return jsonify({"error": "Transaction not found"}), 404
    data = request.json
    transaction.customer_id = data.get('customer_id', transaction.customer_id)
    transaction.product_id = data.get('product_id', transaction.product_id)
    transaction.purchase_date = data.get('purchase_date', transaction.purchase_date)
    db.commit()
    db.refresh(transaction)
    db.close()
    return jsonify({
        "transaction_id": transaction.transaction_id,
        "customer_id": transaction.customer_id,
        "product_id": transaction.product_id,
        "purchase_date": transaction.purchase_date.isoformat() if transaction.purchase_date else None
    })

@transaction_n.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    db = sessionlocal()
    transaction = db.query(Transaction).get(transaction_id)
    if not transaction:
        db.close()
        return jsonify({"error": "Transaction not found"}), 404
    db.delete(transaction)
    db.commit()
    db.close()
    return jsonify({"message": "Transaction deleted"})

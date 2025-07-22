from flask import Blueprint, request, jsonify
from database import sessionlocal
from models.product import Product

product_n = Blueprint('products', __name__)

@product_n.route('/products', methods=['POST'])
def add_product():
    db = sessionlocal()
    data = request.json
    product = Product(
        name=data.get('name'),
        description=data.get('description'),
        price=data.get('price')
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    db.close()
    return jsonify({"product_id": product.product_id})

@product_n.route('/products', methods=['GET'])
def get_all_products():
    db = sessionlocal()
    products = db.query(Product).all()
    db.close()
    return jsonify([
        {
            "product_id": p.product_id,
            "name": p.name,
            "description": p.description,
            "price": p.price
        } for p in products
    ])

@product_n.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    db = sessionlocal()
    product = db.query(Product).get(product_id)
    db.close()
    if product:
        return jsonify({
            "product_id": product.product_id,
            "name": product.name,
            "description": product.description,
            "price": product.price
        })
    return jsonify({"error": "Product not found"}), 404

@product_n.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    db = sessionlocal()
    product = db.query(Product).get(product_id)
    if not product:
        db.close()
        return jsonify({"error": "Product not found"}), 404
    data = request.json
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    db.commit()
    db.refresh(product)
    db.close()
    return jsonify({
        "product_id": product.product_id,
        "name": product.name,
        "description": product.description,
        "price": product.price
    })

@product_n.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    db = sessionlocal()
    product = db.query(Product).get(product_id)
    if not product:
        db.close()
        return jsonify({"error": "Product not found"}), 404
    db.delete(product)
    db.commit()
    db.close()
    return jsonify({"message": "Product deleted"})

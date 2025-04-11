
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

receipts = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.get_json()
    if not receipt:
        return jsonify({'error': 'The receipt is invalid'}), 400
    
    required = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']
    for feild in required:
        if feild not in receipt:
            return jsonify({'error': 'The receipt is invalid'}), 400
    
    id = str(uuid.uuid4())
    receipts[id] = receipt
    
    return jsonify({'id': id}), 200


@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    if id not in receipts:
        return jsonify({'error': 'No receipt found for that ID'}), 404
    
    points = calculate_points(id)

    return jsonify({'points': points}), 200

    
def calculate_points(id):
    receipt = receipts.get(id)
    

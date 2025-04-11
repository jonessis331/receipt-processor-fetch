
from flask import Flask, request, jsonify
import uuid
import math 
import datetime

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
    
    item_fields = ['shortDescription', 'price']
    for field in item_fields:
        if field not in receipt['items']:
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
    points  = 0

    # One point for every alphanumeric character in the retailer name.
    for c in receipt['retailer']:
        if c.isalpha:
            points+=1 

    # 50 points if the total is a round dollar amount with no cents.
    total = float(receipt['total'])
    if total == int(total):
        points+=50
    
    # 25 points if the total is a multiple of 0.25.
    if total % 0.25 == 0:
        points +=25
    # 5 points for every two items on the receipt.
    item_count = len(receipt['items'])
    points += (item_count // 2) * 5
    
    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in receipt['item']:
        if len(item['shortDescription']) % 3 == 0:
            price = float(item['price'])
            points += math.ceil(price * 0.2)

    # 6 points if the day in the purchase date is odd.
   
    date =  receipt['purchaseDate']
    day = int(date.split("-")[2])
    if day % 2 != 0:
        points+=6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    time_purchased = datetime.striptime(receipt['purchaseTime'], '%H:%M')
    two = datetime.strptime('14:00', '%H:%M')
    four = datetime.strptime('16:00', '%H:%M')
    if two.time() < time_purchased.time() < four.time():
        points += 10
        
    return points

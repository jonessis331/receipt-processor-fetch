
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
        
    if not receipt['items']:
        return jsonify({'error': 'The receipt is invalid'}), 400

    for item in receipt['items']:
        if 'shortDescription' not in item or 'price' not in item:
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
        if c.isalnum():
            points+=1
            print(1, points)

    # 50 points if the total is a round dollar amount with no cents.
    total = float(receipt['total'])
    if total == int(total):
        points+=50
        print(2, points)
    
    # 25 points if the total is a multiple of 0.25.
    if total % 0.25 == 0:
        points +=25
        print(3, points)

    # 5 points for every two items on the receipt.
    item_count = len(receipt['items'])
    points += (item_count // 2) * 5
    print(4, points)
    
    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in receipt['items']:
        print(len(item['shortDescription'].lstrip()))
        if len(item['shortDescription'].strip()) % 3 == 0:
            price = float(item['price'])
            points += math.ceil(price * 0.2)
            print(item['shortDescription'])
            print(5, points)

    # 6 points if the day in the purchase date is odd.
    date_purchased =  receipt['purchaseDate']
    day = int(date_purchased.split("-")[2])
    if day % 2 != 0:
        points+=6
        print(6, points)

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    time_purchased = datetime.datetime.strptime(receipt['purchaseTime'], '%H:%M')
    two = datetime.datetime.strptime('14:00', '%H:%M')
    four = datetime.datetime.strptime('16:00', '%H:%M')
    if two.time() < time_purchased.time() < four.time():
        points += 10
        print(7, points)
        
    return points


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)

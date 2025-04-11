import pytest
from receipt_processor_app import app  

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

valid_receipts = [
    {
        "input": {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
            ],
            "total": "35.35"
        },
        "expected_points": 28
    },
    {
        "input": {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"}
            ],
            "total": "9.00"
        },
        "expected_points": 109
    },
    {
        "input": {
            "retailer": "Whole Foods",
            "purchaseDate": "2022-12-15",
            "purchaseTime": "15:00",
            "items": [
                {"shortDescription": "Organic Milk", "price": "4.25"},
                {"shortDescription": "Granola", "price": "6.00"}
            ],
            "total": "10.25"
        },
        "expected_points": 57 
    },
    {
        "input": {
            "retailer": "7Eleven",
            "purchaseDate": "2022-08-03",
            "purchaseTime": "09:45",
            "items": [
                {"shortDescription": "Soda", "price": "1.00"},
                {"shortDescription": "Chips", "price": "1.50"},
                {"shortDescription": "Candy", "price": "2.00"}
            ],
            "total": "4.50"
        },
        "expected_points": 43  
    }
]

@pytest.mark.parametrize("case", valid_receipts)
def test_valid_receipts(client, case):
    post = client.post("/receipts/process", json=case["input"])
    assert post.status_code == 200
    receipt_id = post.get_json().get("id")
    assert receipt_id

    get = client.get(f"/receipts/{receipt_id}/points")
    assert get.status_code == 200
    assert get.get_json()["points"] == case["expected_points"]


invalid_receipts = [
    ({}, 400),  # completely missing body
    ({
        "retailer": "Walmart"
    }, 400),  # missing everything but retailer
    ({
        "retailer": "Walmart",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "10:00",
        "items": [],
        "total": "10.00"
    }, 400),  # no items
    ({
        "retailer": "Walmart",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "10:00",
        "items": [{"price": "3.00"}],  # no shortdescription
        "total": "10.00"
    }, 400),
    ({
        "retailer": "Walmart",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "10:00",
        "items": [{"shortDescription": "Bread"}],  # no price
        "total": "10.00"
    }, 400),
]

@pytest.mark.parametrize("payload,status", invalid_receipts)
def test_invalid_receipts(client, payload, status):
    res = client.post("/receipts/process", json=payload)
    assert res.status_code == status

# 404

def test_points_not_found(client):
    res = client.get("/receipts/nonexistent-id/points")
    assert res.status_code == 404

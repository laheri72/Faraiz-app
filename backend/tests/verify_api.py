import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_calculate():
    payload = {
        "estate_value": 120000,
        "heirs": [
            {"relation": "Father", "gender": "M", "count": 1},
            {"relation": "Mother", "gender": "F", "count": 1}
        ]
    }
    response = client.post("/api/calculate", json=payload)
    print("\n--- API Test: POST /calculate ---")
    print(f"Status: {response.status_code}")
    print(f"Data: {response.json()}")
    
    if response.status_code == 200:
        case_id = response.json()["case_id"]
        # Now verify GET
        get_response = client.get(f"/api/cases/{case_id}")
        print("\n--- API Test: GET /cases/{id} ---")
        print(f"Status: {get_response.status_code}")
        print(f"Data: {get_response.json()}")

if __name__ == "__main__":
    test_api_calculate()

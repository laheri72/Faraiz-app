import httpx
import json

def test_calculate():
    url = "http://127.0.0.1:8000/api/calculate"
    payload = {
        "estate_value": 72000,
        "debts": 0,
        "wasiyyah": 0,
        "heirs": [
            {"relation": "Father", "gender": "M", "count": 1},
            {"relation": "Mother", "gender": "F", "count": 1},
            {"relation": "Son", "gender": "M", "count": 1}
        ]
    }
    
    print(f"Sending request to {url}...")
    try:
        response = httpx.post(url, json=payload, timeout=10.0)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_calculate()

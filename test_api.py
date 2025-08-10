import requests
import json

def test_predict_endpoint(symbol="AAPL"):
    """
    Makes a direct request to the /predict endpoint to test the backend.
    """
    print(f"--- Testing /predict/{symbol} endpoint ---")
    url = f"http://localhost:8000/predict/{symbol}"
    try:
        response = requests.get(url, timeout=30)

        print(f"Status Code: {response.status_code}")
        response.raise_for_status() # Raise an exception for bad status codes

        response_json = response.json()
        print("Response JSON:")
        print(json.dumps(response_json, indent=2))

        # Check for key fields
        assert "ensemble_prediction" in response_json
        assert "recommendation" in response_json
        print("\n--- Backend Test Succeeded ---")

    except Exception as e:
        print(f"\n--- Backend Test FAILED ---")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_predict_endpoint()

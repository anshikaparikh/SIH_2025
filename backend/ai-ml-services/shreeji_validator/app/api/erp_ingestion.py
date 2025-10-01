import requests
import os

# 1️⃣ Read ERP URL and API Key from environment variables or config
ERP_API_URL = os.getenv("ERP_API_URL", "https://erp.example.com/api/data")
ERP_API_KEY = os.getenv("ERP_API_KEY", "your_api_key_here")

def fetch_erp_data(endpoint="students", test_mode=False):
    """
    Fetch bulk data from ERP system.
    If test_mode=True, returns dummy data for testing without ERP connection.
    """
    if test_mode:
        # Dummy data for testing
        return [
            {"student_id": "S101", "name": "Alice", "degree": "B.Tech", "marks": 85},
            {"student_id": "S102", "name": "Bob", "degree": "B.Sc", "marks": 90},
        ]

    url = f"{ERP_API_URL}/{endpoint}"
    headers = {"Authorization": f"Bearer {ERP_API_KEY}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"[ERP Fetch Error] {e}")
        return None

# 🔹 Quick test
if __name__ == "__main__":
    # For testing without real ERP, set test_mode=True
    students = fetch_erp_data(test_mode=True)
    print("ERP Students Data:", students)

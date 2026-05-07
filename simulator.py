import requests
import random
import time
from datetime import datetime

PROJECT_ID = "smartbin-4328b"
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

bins = [
    {"bin_id": "BIN_001", "location": "Main Street"},
    {"bin_id": "BIN_002", "location": "Park Avenue"},
    {"bin_id": "BIN_003", "location": "Central Mall"},
]

def get_status(fill_level):
    if fill_level >= 80:
        return "FULL - Needs Collection"
    elif fill_level >= 50:
        return "MEDIUM"
    else:
        return "OK"

def send_to_firebase(bin_data):
    try:
        doc_id = bin_data["bin_id"]
        url = f"{FIRESTORE_URL}/bins/{doc_id}"
        payload = {
            "fields": {
                "bin_id":     {"stringValue": bin_data["bin_id"]},
                "location":   {"stringValue": bin_data["location"]},
                "fill_level": {"integerValue": bin_data["fill_level"]},
                "status":     {"stringValue": bin_data["status"]},
                "timestamp":  {"stringValue": bin_data["timestamp"]}
            }
        }
        response = requests.patch(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✓ Updated {bin_data['bin_id']} at {bin_data['location']} - Fill: {bin_data['fill_level']}% - {bin_data['status']}")
        else:
            print(f"✗ Error {response.status_code}: {response.text}")
    except requests.exceptions.SSLError:
        print(f"⚠ SSL Error for {bin_data['bin_id']} — WiFi issue, retrying next round...")
    except requests.exceptions.ConnectionError:
        print(f"⚠ No internet for {bin_data['bin_id']} — will retry next round...")
    except requests.exceptions.Timeout:
        print(f"⚠ Timeout for {bin_data['bin_id']} — will retry next round...")
    except Exception as e:
        print(f"⚠ Unexpected error: {e}")

print("=" * 50)
print("  SmartBin IoT Simulator Started")
print("  Sending data to Firebase every 10 seconds")
print("  Press Ctrl+C to stop")
print("=" * 50 + "\n")

while True:
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Updating all bins...")
        for b in bins:
            fill_level = random.randint(0, 100)
            status = get_status(fill_level)
            data = {
                "bin_id": b["bin_id"],
                "location": b["location"],
                "fill_level": fill_level,
                "status": status,
                "timestamp": datetime.now().isoformat()
            }
            send_to_firebase(data)
        print("\n--- Waiting 10 seconds ---\n")
    except KeyboardInterrupt:
        print("\nSimulator stopped.")
        break
    except Exception as e:
        print(f"⚠ General error: {e}")
    time.sleep(10)
import requests
import random
import time

# Configuration
BASE_URL = "http://127.0.0.1:8000"
OBTAIN_TOKEN_URL = f"{BASE_URL}/api/token/"
REFRESH_TOKEN_URL = f"{BASE_URL}/api/token/refresh/"
SENSORS_URL = f"{BASE_URL}/api/sensors/"
READING_URL = f"{BASE_URL}/api/readings/"

CREDENTIALS = {"username": "farmer1", "password": "Test@123"}

class SensorClient:
    def __init__(self):
        self.access = None
        self.refresh = None
        self.sensor_ids = []
        self.authenticate()
        self.fetch_valid_sensors()

    def authenticate(self):
        """Initial login to get both tokens."""
        print("Logging in for initial tokens...")
        r = requests.post(OBTAIN_TOKEN_URL, json=CREDENTIALS)
        if r.status_code == 200:
            data = r.json()
            self.access = data['access']
            self.refresh = data['refresh']
        else:
            raise Exception(f"Login failed: {r.text}")

    def refresh_access_token(self):
        """Uses the refresh token to get a new access token."""
        print("Access token expired. Refreshing...")
        r = requests.post(REFRESH_TOKEN_URL, json={"refresh": self.refresh})
        if r.status_code == 200:
            self.access = r.json()['access']
            return True
        else:
            print("Refresh token expired. Must re-authenticate.")
            self.authenticate()
            return True

    def fetch_valid_sensors(self):
        """Fetches available sensors and extracts their IDs from paginated response."""
        headers = {"Authorization": f"Bearer {self.access}"}
        try:
            response = requests.get(SENSORS_URL, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            results = data.get('results', [])
            self.sensor_ids = [s['id'] for s in results]
            
            print(f"Found {len(self.sensor_ids)} valid sensors: {self.sensor_ids}")
        except Exception as e:
            print(f"Failed to fetch sensors: {e}")

    def send_data(self):
        if not self.sensor_ids:
            print("No valid sensors found to send data for.")
            return

        sensor_id = random.choice(self.sensor_ids)
        payload = {
            "sensor": sensor_id,
            "temperature": round(random.uniform(1, 50), 2)
        }
        
        headers = {"Authorization": f"Bearer {self.access}"}
        
        try:
            response = requests.post(READING_URL, json=payload, headers=headers)
            
            # If 401, the access token likely expired
            if response.status_code == 401:
                if self.refresh_access_token():
                    # Retry the request once with the new token
                    headers["Authorization"] = f"Bearer {self.access}"
                    response = requests.post(READING_URL, json=payload, headers=headers)
            
            if response.status_code == 201:
                print(f"Sensor {sensor_id}: {payload['temperature']}°C")
            else:
                print(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")

if __name__ == "__main__":
    client = SensorClient()
    while True:
        client.send_data()
        time.sleep(10)

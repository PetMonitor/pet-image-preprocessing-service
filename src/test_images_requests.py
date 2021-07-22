import requests
import uuid

BASE = "http://127.0.0.1:5000/api/v0/"
user_id = uuid.uuid4()

# POST images
response1 = requests.post(BASE + "preprocessed-images", data={'petImages': []})
new_report = response1.json()
assert response1.status_code == 200
print(new_report)


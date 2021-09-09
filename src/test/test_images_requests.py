import requests
import uuid
import base64

filename = 'dog.jpeg'
# filename = 'two_dogs.jpg'
with open(filename, "rb") as image2string:
    converted_string = base64.b64encode(image2string.read())

BASE = "http://127.0.0.1:5000/api/v0/"
user_id = uuid.uuid4()

# POST images
response1 = requests.post(BASE + "preprocessed-images", data={'petImages': [converted_string.decode()]})
new_report = response1.json()
assert response1.status_code == 200
print(new_report)

results = new_report['petImages'][0]
for i in range(len(results)):
    with open(f'result_{i}_{filename}', "wb") as fh:
        fh.write(base64.decodebytes(results[i].encode()))


import requests
import uuid
import base64

filename1 = 'dog.jpeg'
filename2 = 'two_dogs.jpg'
# filename = 'milka.jpg'
files = [filename1, filename2]
img_strings = []
for file in files:
    with open(file, "rb") as image2string:
        img_strings.append(base64.b64encode(image2string.read()).decode())

BASE = "http://127.0.0.1:5000/api/v0/"
user_id = uuid.uuid4()

# POST images
response1 = requests.post(BASE + "preprocessed-images", data={'petImages': img_strings})
img_results = response1.json()
print(img_results)
assert response1.status_code == 200

results = img_results['petImages']
for i in range(len(results)):
    for j in range(len(results[i])):
        with open(f'result_{i}_{j}.jpg', "wb") as fh:
            fh.write(base64.decodebytes(results[i][j].encode()))

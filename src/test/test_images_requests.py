import requests
import uuid
import base64
import os

directory = 'photos_to_process'
img_strings = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        with open(f, "rb") as image2string:
            img_strings.append(base64.b64encode(image2string.read()).decode())


# for file in files:
#     with open(file, "rb") as image2string:
#         img_strings.append(base64.b64encode(image2string.read()).decode())

BASE = "http://127.0.0.1:5000/api/v0/"
user_id = uuid.uuid4()

# POST images
response1 = requests.post(BASE + "preprocessed-images", data={'petImages': img_strings})
img_results = response1.json()
# print(img_results)
assert response1.status_code == 200

results = img_results['petImages']
id = 100
counter = 0
for i in range(len(results)):
    for j in range(len(results[i])):
        with open(f'photos_res/{id}.{counter}.png', "wb") as fh:
            fh.write(base64.decodebytes(results[i][j].encode()))
            counter = counter + 1

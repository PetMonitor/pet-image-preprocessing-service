import requests
import uuid
import base64

file = 'dog.jpeg'
with open(file, "rb") as image2string:
    converted_string = base64.b64encode(image2string.read())
# image = open(file, 'rb')
# image_read = image.read()
# image_64_encode = base64.encodebytes(image_read) #encodestring also works aswell as decodestring

print('This is the image in base64: ' + (str(converted_string)))
print('This is the image in base64: ' + converted_string.decode())

BASE = "http://127.0.0.1:5000/api/v0/"
user_id = uuid.uuid4()

# POST images
response1 = requests.post(BASE + "preprocessed-images", data={'petImages': [converted_string.decode()]})
new_report = response1.json()
assert response1.status_code == 200
print(new_report)

with open("imageToSave.jpg", "wb") as fh:
    fh.write(base64.decodebytes(new_report['petImages'][0].encode()))


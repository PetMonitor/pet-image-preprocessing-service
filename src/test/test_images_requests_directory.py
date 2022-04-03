import requests
import uuid
import base64
import os


filename1 = 'atowata/1.jpg'
filename2 = 'atowata/2.jpg'
filename3 = 'atowata/3.jpg'
filename4 = 'atowata/4.jpg'
filename5 = 'atowata/5.jpg'
filename6 = 'atowata/6.jpg'
filename7 = 'atowata/7.jpg'
filename8 = 'atowata/8.jpg'
filename9 = 'atowata/9.jpg'
filename10 = 'atowata/10.jpg'
filename11 = 'atowata/11.jpg'
filename12 = 'atowata/12.jpg'
filename13 = 'atowata/13.jpg'
filename14 = 'atowata/14.jpg'
filename15 = 'atowata/15.jpg'

directory = 'dir_to_process'


files = [filename1, filename2, filename3, filename4, filename5, filename6, filename7, filename8, filename9, filename10, filename11, filename12]
# files = [filename1, filename2, filename3, filename4, filename5, filename6, filename7, filename8, filename9, filename10, filename11, filename12, filename13, filename14, filename15]


BASE = "http://127.0.0.1:5000/api/v0/"
user_id = uuid.uuid4()

for subdir in os.listdir(directory):
    img_strings = []
    subdir_path = os.path.join(directory, subdir)

    for file in os.listdir(subdir_path):
        file_path = os.path.join(subdir_path, file)
        # checking if it is a file
        if os.path.isfile(file_path):
            with open(file_path, "rb") as image2string:
                img_strings.append(base64.b64encode(image2string.read()).decode())


    res_path = subdir_path.replace(directory, "dir_results")
    print("# of images " + str(len(img_strings)))
    os.mkdir(res_path)
    print("creating dir for " + res_path)
    # POST images of the subdir
    response1 = requests.post(BASE + "preprocessed-images", data={'petImages': img_strings})
    img_results = response1.json()
    # print(img_results)
    # assert response1.status_code == 200

    results = img_results['petImages']
    counter = 0
    for i in range(len(results)):
        for j in range(len(results[i])):
            with open(f'dir_results/{subdir}/{subdir}.{counter}.png', "wb") as fh:
                fh.write(base64.decodebytes(results[i][j].encode()))
                counter = counter + 1





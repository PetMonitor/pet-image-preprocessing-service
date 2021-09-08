import base64
import math

import dlib, cv2, os
import io
import imutils as imutils
from imutils import face_utils
import numpy as np
import matplotlib.pyplot as plt
import imutils
from imageio import imread

# Load Models
detector = dlib.cnn_face_detection_model_v1('src/dog_face_detector/dogHeadDetector.dat')
predictor = dlib.shape_predictor('src/dog_face_detector/landmarkDetector.dat')

def detect_dog_face_from_file():
    # Load Dog Image
    img_path = 'img/19.jpg'
    # img_path = 'img/test-flip.png'
    filename, ext = os.path.splitext(os.path.basename(img_path))
    img = cv2.imread(img_path)
    detect_dog_face(img, filename, ext)

def detect_dog_face_from_string(image):
    img = imread(io.BytesIO(base64.b64decode(image)))

    # nparr = np.fromstring(image, np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # print(type(img))
    cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # cv2.imwrite("reconstructed.jpg", cv2_img)
    return detect_dog_face(cv2_img, 'testing', '.jpg')

def detect_dog_face(img, filename, ext):
    h, w, _ = img.shape
    if h > 1000 or w > 1000:
        # new code to resize image but keeping the aspect ratio at the same time
        img = imutils.resize(img, width=1000)

    # Change image from BGR (blue, green, red) to RGB (red, green, blue)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.resize(img, dsize=None, fx=0.5, fy=0.5)

    plt.figure(figsize=(16, 16))
    plt.imshow(img)
    # plt.show()

    # Detect Faces
    dets = detector(img, upsample_num_times=1)

    print(dets)

    # Create a copy of the image
    img_result = img.copy()
    # dets = [dets[0]]
    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(i, d.rect.left(), d.rect.top(),
                                                                                          d.rect.right(), d.rect.bottom(),
                                                                                          d.confidence))
        # Rectangle coordinates
        x1, y1 = d.rect.left(), d.rect.top()
        x2, y2 = d.rect.right(), d.rect.bottom()
        # Print rectangle => we should rotate first and then crop
        cv2.rectangle(img_result, pt1=(x1, y1), pt2=(x2, y2), thickness=2, color=(255, 0, 0), lineType=cv2.LINE_AA)

    if len(dets) > 0:
        y1 = y1 if y1 >= 0 else 0
        x1 = x1 if x1 >= 0 else 0
        # crop_img = img[y1 - 50 if y1 - 50 > 0 else 0:y2 + 50, x1 - 50 if x1 - 50 > 0 else 0:x2 + 50]
        # crop_img = img[y1:y2, x1:x2]


        # Detect Landmarks
        shapes = []
        for i, d in enumerate(dets):
            shape = predictor(img, d.rect)
            shape = face_utils.shape_to_np(shape)
            shapes.append(shape)

            for i, p in enumerate(shape):
                cv2.circle(img_result, center=tuple(p), radius=3, color=(0, 0, 255), thickness=-1, lineType=cv2.LINE_AA)
                cv2.putText(img_result, str(i), tuple(p), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        img_out = cv2.cvtColor(img_result, cv2.COLOR_RGB2BGR)
        cv2.imwrite('src/dog_face_detector/img/%s_out%s' % (filename, ext), img_out)
        plt.figure(figsize=(16, 16))
        plt.imshow(img_result)

        right_eye = shapes[0][5]
        left_eye = shapes[0][2]

        print(shapes)
        dx = left_eye[0] - right_eye[0]
        dy = -(left_eye[1] - right_eye[1]) # we flip this since image has (0,0) in top left corner instead of bottom left corner like in math

        alpha = math.degrees(math.atan2(dy, dx))

        (h, w) = img_result.shape[:2]
        (cX, cY) = right_eye[:2]
        print(cX)
        print(cY)
        M = cv2.getRotationMatrix2D((int(cX), int(cY)), -alpha, 1.0)

        input_points = np.array([[[x1, y1]], [[x2, y2]]])
        print(input_points)
        result = cv2.transform(input_points, M)
        print(result)

        img_result2 = img.copy()
        img_3 = cv2.warpAffine(img_result2, M, (w, h))

        # COMMENT TO SEE ROTATION POINTS
        # cv2.circle(img_3, center=tuple(result[0][0]), radius=3, color=(0, 0, 255), thickness=-1, lineType=cv2.LINE_AA)
        # cv2.putText(img_3, "res x1, y1", tuple(result[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
        #             cv2.LINE_AA)
        # cv2.circle(img_3, center=tuple(result[1][0]), radius=3, color=(0, 0, 255), thickness=-1, lineType=cv2.LINE_AA)
        # cv2.putText(img_3, "res x2, y2", tuple(result[1][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
        #             cv2.LINE_AA)
        plt.figure(figsize=(16, 16))
        plt.imshow(img_3)
        # plt.show()

        new_x2 = result[1][0][0]
        new_x1 = result[0][0][0]
        new_y2 = result[1][0][1]
        new_y1 = result[0][0][1]
        dx = new_x2 - new_x1
        dy = new_y2 - new_y1

        dif = abs(dx - dy)
        if dx > dy:
            new_y1 = new_y1 - (dif // 2)
            new_y2 = new_y2 + (dif // 2)
        if dy > dx:
            new_x1 = new_x1 - (dif // 2)
            new_x2 = new_x2 + (dif // 2)
        img_3 = img_3[new_y1 if new_y1 >= 0 else 0 :new_y2, new_x1 if new_x1 >= 0 else 0:new_x2]

        img_3 = cv2.resize(img_3, (224, 224))
        img_out2 = cv2.cvtColor(img_3, cv2.COLOR_RGB2BGR)

        cv2.imwrite('src/dog_face_detector/rot-test/%s_out2%s' % (filename, ext), img_out2)

        _, buffer_img = cv2.imencode('.png', img_out2)
        return base64.b64encode(buffer_img).decode()


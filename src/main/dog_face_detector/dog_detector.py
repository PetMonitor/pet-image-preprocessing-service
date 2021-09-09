import base64
import math

import dlib, cv2
import io
from imutils import face_utils
import numpy as np
import imutils
from imageio import imread

# Load Models
detector = dlib.cnn_face_detection_model_v1('src/main/dog_face_detector/dogHeadDetector.dat')
predictor = dlib.shape_predictor('src/main/dog_face_detector/landmarkDetector.dat')

def detect_dog_face_from_file(img_path):
    # Load Dog Image
    # img_path = 'img/19.jpg'
    # filename, ext = os.path.splitext(os.path.basename(img_path))
    img = cv2.imread(img_path)
    return detect_dog_face(img)

def detect_dog_face_from_string(image):
    img = imread(io.BytesIO(base64.b64decode(image)))
    cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return detect_dog_face(cv2_img)

def detect_dog_face(img):
    h, w, _ = img.shape
    if h > 500 or w > 500:
        # new code to resize image but keeping the aspect ratio at the same time
        img = imutils.resize(img, width=500)

    # Change image from BGR (blue, green, red) to RGB (red, green, blue)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect Faces
    dets = detector(img, upsample_num_times=1)
    results = []
    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(i, d.rect.left(), d.rect.top(),
                                                                                          d.rect.right(), d.rect.bottom(),
                                                                                          d.confidence))
        # Rectangle coordinates
        x1, y1 = d.rect.left(), d.rect.top()
        x2, y2 = d.rect.right(), d.rect.bottom()

        y1 = y1 if y1 >= 0 else 0
        x1 = x1 if x1 >= 0 else 0

        # Detect Landmarks
        shape = predictor(img, d.rect)
        shape = face_utils.shape_to_np(shape)

        right_eye = shape[5]
        left_eye = shape[2]
        dx = left_eye[0] - right_eye[0]
        dy = -(left_eye[1] - right_eye[1]) # we flip this since image has (0,0) in top left corner instead of bottom left corner like in math
        alpha = math.degrees(math.atan2(dy, dx))

        (h, w) = img.shape[:2]
        (cX, cY) = right_eye[:2]
        M = cv2.getRotationMatrix2D((int(cX), int(cY)), -alpha, 1.0)

        input_points = np.array([[[x1, y1]], [[x2, y2]]])
        result = cv2.transform(input_points, M)

        # Create a copy of the image
        img_result = img.copy()
        img_result = cv2.warpAffine(img_result, M, (w, h))

        # COMMENT TO SEE ROTATION POINTS
        # cv2.circle(img_3, center=tuple(result[0][0]), radius=3, color=(0, 0, 255), thickness=-1, lineType=cv2.LINE_AA)
        # cv2.putText(img_3, "res x1, y1", tuple(result[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
        #             cv2.LINE_AA)
        # cv2.circle(img_3, center=tuple(result[1][0]), radius=3, color=(0, 0, 255), thickness=-1, lineType=cv2.LINE_AA)
        # cv2.putText(img_3, "res x2, y2", tuple(result[1][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
        #             cv2.LINE_AA)

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
        img_result = img_result[new_y1 if new_y1 >= 0 else 0 :new_y2, new_x1 if new_x1 >= 0 else 0:new_x2]

        img_result = cv2.resize(img_result, (224, 224))
        img_result = cv2.cvtColor(img_result, cv2.COLOR_RGB2BGR)

        _, buffer_img = cv2.imencode('.png', img_result)
        results.append(base64.b64encode(buffer_img).decode())

    return results

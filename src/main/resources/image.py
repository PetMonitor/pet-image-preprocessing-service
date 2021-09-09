import http

from flask_restful import fields, reqparse, Resource, marshal_with
from src.dog_face_detector.dog_detector import detect_dog_face_from_string

# Fields returned by the src for the Images resource
images_fields = {
    'petImages': fields.List(cls_or_instance=fields.List(cls_or_instance=fields.String))
}

class Images(Resource):

    def __init__(self):
        # Argument parser for Images pre-processing JSON body
        self.create_args = _create_images_request_parser()
        super(Images, self).__init__()


    @marshal_with(images_fields)
    def post(self):
        """
        Retrieves pet images and applies pre-processing operations to them.
        :returns the processed images that will be ready as input of the model.
        """
        args = self.create_args.parse_args()
        images_to_process = args['petImages']
        preprocessed_images = []
        for image in images_to_process:
            preprocessed_images.append(detect_dog_face_from_string(image))
        return {
                   'petImages': preprocessed_images
               }, http.HTTPStatus.OK


def _create_images_request_parser():
    images_request_parser = reqparse.RequestParser()
    images_request_parser.add_argument("petImages", type=str, action='append', help="The images are required", required=True)
    return images_request_parser

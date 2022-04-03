import os
from flask import Flask
from flask_restful import Api

from src.main.resources.image import Images

app = Flask(__name__)
api = Api(app, prefix='/api/v0')


# We define all the endpoints handled by this service
api.add_resource(Images, '/preprocessed-images')

if __name__ == '__main__':
    os.environ["FLASK_RUN_PORT"] = 5002
    app.run()

'''
from src import api

from src.main.resources.image import Images

# We define all the endpoints handled by this service
api.add_resource(Images, '/preprocessed-images')
'''

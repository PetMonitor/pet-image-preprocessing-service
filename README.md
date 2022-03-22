# Pet Image Pre-processing Service
Server that preprocess the pet images, applying cropping, resizing and rotations to make them suitable for the recognition model.

# Run project locally

- Create virtual environment in this directory:
    `python3 -m venv .`
- Activate virtual environment
    `source bin/activate`
- Install dependencies
    `python3 -m pip install -r requirements.txt`

- Run flask app:
    - `export FLASK_APP=src.main.routes.py`
    - `export FLASK_RUN_PORT=5002`
    - `flask run`

# Troubleshooting

If it fails with an error in cv2 saying it is unable to find 'image', try this:

- `python3 -m pip install --force-reinstall opencv-python`
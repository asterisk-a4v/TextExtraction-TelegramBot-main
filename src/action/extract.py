from json import load

from google.cloud import vision
from google.oauth2 import service_account


def image_to_text(image_path):

    with open("config.json", "r") as config_file:
        config = load(config_file)

    credentials = service_account.Credentials.from_service_account_info(config)

    # Create a client for the Vision API
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # Load an image file
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    # Perform text detection on the image
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    return response

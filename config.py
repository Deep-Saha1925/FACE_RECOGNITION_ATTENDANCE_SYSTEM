from dotenv import load_dotenv
import os

load_dotenv()  # load variables from .env into environment

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

CREDENTIAL_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
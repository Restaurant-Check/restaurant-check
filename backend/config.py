import os

class Config:
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
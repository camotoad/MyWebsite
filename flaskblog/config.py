import os

class Config:
    SECRET_KEY = os.environ.get('SK_FlaskBlog')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mywebsite.db'
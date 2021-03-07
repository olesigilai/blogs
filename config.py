import os

class Config:
    BASE_URL='http://quotes.stormconsultancy.co.uk/random.json'
    SECRET_KEY = os.environ.get("SECRET_KEY")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST ='app/static/photos'

    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME =os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD =os.environ.get("MAIL_PASSWORD")
    
    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("HEROKU_POSTGRESQL_GREEN_URL")

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:kipkirui@localhost/blogs_test'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:kipkirui@localhost/blogs'
    
    DEBUG = True
config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}

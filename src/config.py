import os

class Config:
    
    SECRET_KEY=os.getenv('SECRET_KEY')

class productionConfig(Config):

    DEBUG=True
    MYSQL_HOST=os.getenv('MYSQL_HOST')
    MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD')
    MYSQL_USER=os.getenv('MYSQL_USER')
    MYSQL_DB=os.getenv('MYSQL_DB')

config = {
    "production": productionConfig
}
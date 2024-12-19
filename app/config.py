import os

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = "root"
PASSWORD = "111111"
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'classroom_student_monitoring_system'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.environ.get('SECRET_KEY') or '1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p'

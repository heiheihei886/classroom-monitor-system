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

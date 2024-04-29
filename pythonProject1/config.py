
SECRET_KEY = "sdafewafewwqfgdsf"

# 数据库的配置信息

HOSTNAME = "172.30.84.104"
PORT = 3306
USERNAME = "root"
PASSWORD = "877274"
DATABASE = "app"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

#uhyduvynwpkuifdg

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USERNAME = "1300943104@qq.com"
MAIL_PASSWORD = "uhyduvynwpkuifdg"
MAIL_DEFAULT_SENDER = "1300943104@qq.com"
MAIL_USE_SSL = True

PER_PAGE_COUNT = 10
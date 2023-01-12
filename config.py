import os


host = os.getenv("host",default=None)
user = os.getenv("user",default=None)
passwd = os.getenv("passwd",default=None)
database = os.getenv("database",default=None)

db_pwd = os.getenv("db_pwd",default=None)
courier_api = os.getenv("courier_api",default=None)

myemail = os.getenv("myemail",default=None)
drop_box_id = os.getenv("drop_box_id",default=None)
drop_box_pwd = os.getenv("drop_box_pwd",default=None)


drop_token = os.getenv("drop_token",default=None)

mongo_str = os.getenv("mongo_str",default=None)
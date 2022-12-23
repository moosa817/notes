from flask import Flask,session
import os
import config
from flask_files.signup import signup_page
from flask_files.login import login_page,reset_page
from flask_files.index import index_page
from flask_files.notes import notes_page
from flask_files.index_edit import index_edit_page,delete_name_page,view_page,download_name_page
from flask_files.profile import profile_page,profile_edit_page,verify_page
from flask_files.mymedia import media_page
from flask_files.admin import admin_page



UPLOAD_FOLDER = 'static/imgs'
b = os.getcwd()
# print(os.listdir())
UPLOAD_FOLDER = os.path.join(b, UPLOAD_FOLDER) 

# create flask app
app = Flask(__name__)

# mail = Mail(app) # instantiate the mail class
   
# # configuration of mail
# app.config['MAIL_SERVER']= config.MAIL_SERVER
# # app.config['MAIL_PORT'] = config.MAIL_PORT
# app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
# app.config['MAIL_PASSWORD'] = config.MAIL_PWD
# app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
# app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL









app.register_blueprint(signup_page)
app.register_blueprint(login_page)
app.register_blueprint(reset_page)
app.register_blueprint(index_page)
app.register_blueprint(notes_page)

app.register_blueprint(index_edit_page)
app.register_blueprint(delete_name_page)
app.register_blueprint(view_page)
app.register_blueprint(download_name_page)


app.register_blueprint(profile_page)
app.register_blueprint(profile_edit_page)
app.register_blueprint(verify_page)


app.register_blueprint(media_page)

app.register_blueprint(admin_page)


app.secret_key = "super secret key"
app.url_map.strict_slashes = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

app.secret_key = "super secret key"
app.url_map.strict_slashes = False



@app.before_request
def make_session_permanent():
    session.permanent = True 


if __name__ == '__main__':
    # context = ('server.crt', 'server.key')#certificate and key files
    
    app.run(host="0.0.0.0",debug=True, port=os.getenv("PORT", default=5000))
from flask import Flask,session
import os
from flask_files.signup import signup_page
from flask_files.login import login_page
from flask_files.index import index_page
from flask_files.notes import notes_page
from flask_files.index_edit import index_edit_page,delete_name_page,view_page,download_name_page

# create flask app
app = Flask(__name__)

app.register_blueprint(signup_page)
app.register_blueprint(login_page)
app.register_blueprint(index_page)
app.register_blueprint(notes_page)

app.register_blueprint(index_edit_page)
app.register_blueprint(delete_name_page)
app.register_blueprint(view_page)
app.register_blueprint(download_name_page)

app.secret_key = "super secret key"
app.url_map.strict_slashes = False

@app.before_request
def make_session_permanent():
    session.permanent = True 


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=os.getenv("PORT", default=5000))
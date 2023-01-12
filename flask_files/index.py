from flask import session, request, blueprints, redirect, url_for, render_template
import re
import config
from pymongo import MongoClient



client = MongoClient(config.mongo_str)
db = client.get_database('notes')
records = db.notes_data


index_page = blueprints.Blueprint(
    'index', __name__, static_folder='static', template_folder='templates')


@index_page.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        filename = request.form['filename']
        file_regex = "^[ a-zA-Z0-9_.-]+$"
        if re.match(file_regex, filename) and len(filename) > 0 and len(filename) < 50:

            email = session["email"]

            result = records.find_one({"email":email,"filename":filename})


            o = []

            if not result:
                records.insert_one({"email":email,"filename":filename,"published":False,"editor_data":""})


                session["files"].append(filename)

                return render_template("index.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], success="File Created", files=session["files"])
            else:
                return render_template("index.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], error="File Already Exists", files=session["files"])
        else:
            return render_template("index.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], error="Enter a valid filename", files=session["files"])

    if session.get("username"):
        email = session["email"]

        results = records.find({"email":email})

        files = []
        for i in results:
            files.append(i['filename'])

        session["files"] = files

        return render_template("index.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"])
    else:
        return render_template("index.html")


@index_page.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index.index"))


@index_page.route("/test", methods=["GET", "POST"])
def test():
    return 'sent'

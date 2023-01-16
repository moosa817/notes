from flask import session, request, blueprints, redirect, url_for, render_template,jsonify
import re
import config
from pymongo import MongoClient
import requests
import datetime



client = MongoClient(config.mongo_str)
db = client.get_database('notes')
records = db.notes_data
records_logs = db.logs


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


@index_page.route("/log", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        r = 'https://api.ipify.org?format=json'
        r = requests.get(r)

        ip = r.json()
        ip = ip["ip"]
        if session.get("email"):
            email = session["email"]
        else:
            email = "Guest"

        now = datetime.datetime.now()
        utcnow = datetime.datetime.utcnow()
        diff = utcnow-now

        diff_hr = diff.total_seconds()/60/60
        diff_hr = "{:.1f}".format(diff_hr)

        diff_hr = float(diff_hr)
        diff_hr = int(diff_hr)
   
        def convert(seconds):
            min, sec = divmod(seconds, 60)
            hour, min = divmod(min, 60)
            return '%d:%02d:%02d' % (hour, min, sec)

        time_diff = convert(diff.total_seconds())

        if diff.total_seconds() < 0:
            final_time = now.strftime(f"%a %d %b %H:%M:%S{time_diff}")
        else:
            final_time = now.strftime(f"%a %d %b %H:%M:%S+{time_diff}")

            
        records_logs.insert_one({"email":email,"time":final_time,"ip":ip})
        

        return jsonify({"ok":"sure"})

    return 'A'
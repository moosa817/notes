from flask import session, request, blueprints, redirect, render_template,jsonify
import re
import config
from pymongo import MongoClient
import requests


client = MongoClient(config.mongo_str)
db = client.get_database('notes')
records_media = db.use_media
records = db.notes_data
records_admin = db.logs

admin_page = blueprints.Blueprint(
    'admin_page', __name__, static_folder='static', template_folder='templates')


@admin_page.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("pwd"):
            pwd = request.form["pwd"]
            if pwd == config.db_pwd:
                session["admin"] = True
                return redirect("/admin")
            else:
                return render_template("admin.html", login=False, error="wrong pwd")

        if request.form.get("delete_email"):
            to_delete = request.form.get("delete_email")
            records_media.delete_one({"email":to_delete})

        if request.form.get("input1"):
            input1 = request.form["input1"]
            email = request.form["email"]

            records_media.update_one({"email":email},{"$set":{"status":input1}})

    if session.get("admin"):
        if request.form.get("email1") and request.form.get("email_to_use1") and request.form.get("status1"):
            email = request.form["email1"]
            email_to_use = request.form["email_to_use1"]
            status = request.form["status1"]

            emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if not re.match(emailRegex, email) or not re.match(emailRegex, email_to_use):
                pass
            else:
                records_media.insert_one({"email":email,"email_to_use":email_to_use,"status":status})

        page = request.args.get("page")
        if page == "editor":
            result = records.find({})

            email = []
            filename = []
            editor_data = []
            is_public = []
            id = 0
            ids = []
            for i in result:
                id = id+1
                ids.append(id)
                email.append(i["email"])
                filename.append(i["filename"])
                is_public.append(i["published"])
                editor_data.append(i["editor_data"])

            return render_template("admin.html", login=True, ids=ids, email=email, filename=filename, editor_data=editor_data, page1=True, is_public=is_public)

        elif page == "verify":
            result = records_media.find({})

            email = []
            use_email = []
            status = []
            id = 0
            ids = []
            for i in result:
                id = id+1
                ids.append(id)
                email.append(i["email"])
                use_email.append(i["email_to_use"])
                status.append(i["status"])

            return render_template("admin.html", login=True, ids=ids, email=email, use_email=use_email, status=status, page2=True)

        elif page == "logs":
            email = []
            ip = []
            time = []
            for i in records_admin.find({}):
                email.append(i["email"])
                ip.append(i["ip"])
                time.append(i["time"])
            ids = list(range(1,len(email)))

            return render_template("admin.html", login=True,page3=True,email=email,ip=ip,ids=ids,time=time)
        else:
            return render_template("admin.html", login=True)

    return render_template("admin.html", login=False)

@admin_page.route("/get_info",methods=["POST","GET"])
def get():
    r = requests.get("https://ipinfo.io/json")

    return r.json()
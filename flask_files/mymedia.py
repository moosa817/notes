from flask import session, request, blueprints, redirect, render_template, jsonify
import config
import requests
import base64
from flask_files import dropbox_stuff as Db
import re
from pymongo import MongoClient



client = MongoClient(config.mongo_str)
db = client.get_database('notes')
records = db.use_media


media_page = blueprints.Blueprint(
    'media_page', __name__, static_folder='static', template_folder='templates')

disconnect_page = blueprints.Blueprint(
    'disconnect_page', __name__, static_folder='static', template_folder='templates')


@media_page.route("/media", methods=['GET', 'POST'])
def media():
    if session.get("username"):
        if request.method == "POST":
            if request.form.get("sync"):
                try:
                    mytime = Db.SyncThings(
                        session["access_token"], session["email"])
                    return jsonify({"success": True, "time": mytime})
                except Exception as e:
                    return jsonify({"success": False})
            if request.form.get("email"):
                email = request.form["email"]
                emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

                if not re.match(emailRegex, email):
                    return render_template("mymedia.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], use=False, error="Enter a Valid Email Address")

                records.insert_one({"email":session["email"],"email_to_use":email,"status":"pending"})

                headers = {
                    'Authorization': f'Bearer {config.courier_api}',
                    'Content-Type': 'application/x-www-form-urlencoded',
                }

                data = """{"message": {"to": {"email":"%s"},
                "content": { "title": "Add User To Verification state",  "body": "Add this user on notes for media email: %s , use email is %s"}}}""" % (config.myemail, session["email"], email)

                response = requests.post(
                    'https://api.courier.com/send', headers=headers, data=data)

            if 'file-input' in request.files:

                file = request.files['file-input']
                if file:
                    path = '/Notes-817/' + file.filename
                    g = []
                    for i in session["dp_files"]:
                        g.append(session["dp_files"][i][2])

                    counter = 0
                    while path in g:
                        counter = counter + 1
                        match = re.match(r'(.+)\.([^.]+)$', path)
                        name = match.group(1)
                        ext = match.group(2)
                        path = f"{name}{counter}.{ext}"

                    file_content = file.read()
                    Db.write_file_to_dropbox(
                        session["access_token"], path, file_content)
                    session["dp_files"] = Db.MyStuff(session["access_token"])

            if request.form.get("delete-file"):
                delete_file = request.form["delete-file"]
                name = delete_file.split("/Notes-817/")
                name = name[1]
                if Db.DeleteFile(session["access_token"], delete_file):
                    del session["dp_files"][name]
                else:
                    pass

        can_use = False
        result = records.find_one({"email":session["email"]})

        try:
            result = result[0]
        except:
            result = result

        if not result:
            can_use = False
        else:
            status = result["status"]
            if status == "pending":
                return render_template("mymedia.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], use="pending")
            elif status == "verified":
                can_use = True

        if can_use:
            code = request.args.get("code")
            if code:

                client_creds = f"{config.drop_box_id}:{config.drop_box_pwd}"
                client_creds_bs64 = base64.b64encode(client_creds.encode())

                headers = {
                    "Authorization": f"Basic {client_creds_bs64.decode()}"
                }

                data = {
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": "https://notes817.vercel.app/media"
                }

                r = requests.post(
                    "https://api.dropboxapi.com/oauth2/token", headers=headers, data=data)

                stuff = r.json()
                if r.status_code == 200:
                    access_token = stuff["access_token"]
                    refresh_token = stuff["refresh_token"]

                    session["refresh_token"] = refresh_token
                    session["access_token"] = access_token

                    dp_files = Db.MyStuff(session["access_token"])

                    sync_time = Db.SyncStuff(session["email"])

                    session["dp_files"] = dp_files

                    return render_template("mymedia.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], token=True, use=True, dp_files=dp_files, sync_time=sync_time)
                else:
                    return redirect('/media')

            if session.get("access_token"):
                if Db.validate_token(session["access_token"]):

                    # token is good to go
                    # print("from validate token")
                    if not session.get("dp_files"):
                        dp_files = Db.MyStuff(session["access_token"])
                        session["dp_files"] = dp_files
                    else:
                        dp_files = session["dp_files"]
                        sync_time = Db.SyncStuff(session["email"])

                    return render_template("mymedia.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], token=True, use=True, dp_files=dp_files, sync_time=sync_time)

                else:
                    # refresh token
                    try:
                        session["access_token"] = Db.RefreshToken(
                            session["refresh_token"])
                    except:
                        return render_template("mymedia.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], token=False)

                    if not session.get("dp_files"):
                        dp_files = Db.MyStuff(session["access_token"])
                    else:
                        dp_files = session["dp_files"]

                    sync_time = Db.SyncStuff(session["email"])

                    return render_template("mymedia.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], token=True, use=True, dp_files=dp_files, sync_time=sync_time)

            else:
                return render_template("mymedia.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], use=True, token=False)

        else:
            return render_template("mymedia.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], use=False)

        return render_template("mymedia.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], use=False)
    else:
        return render_template("index.html")


@disconnect_page.route("/disconnect")
def dis():
    session.pop("access_token", default=None)
    session.pop("refresh_token", default=None)
    return redirect("/media")


@disconnect_page.route("/refresh")
def refresh():

    dp_files = Db.MyStuff(session["access_token"])
    session["dp_files"] = dp_files
    return redirect("/media")

from flask import session, request, blueprints, jsonify, render_template, url_for, redirect, flash
from flask import current_app
import requests
import os
import mysql.connector
import config
from werkzeug.utils import secure_filename
import re
import bcrypt
from pysqlcipher3 import dbapi2 as sqlite
import random

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webp', 'tiff'])


def Email_To(email):
    random_no = random.randrange(1, 10**6)

    headers = {
        'Authorization': f'Bearer {config.courier_api}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = """{"message": {"to": {"email":"%s"},
    "content": { "title": "Verify Your Email!",  "body": "Your Verification Code is {{code}}"},"data": {"code": %s }}}""" % (email, random_no)

    response = requests.post(
        'https://api.courier.com/send', headers=headers, data=data)
    return random_no


def update_user(old_username, new_username):
    conn = mysql.connector.connect(
        host=config.host,
        user=config.user,
        passwd=config.passwd,
        database=config.database)
    cursor = conn.cursor()
    sql = "UPDATE notes SET username='%s' WHERE username='%s'"
    val = (new_username, old_username)

    cursor.execute(sql % val)
    conn.commit()
    conn.close()


def update_password(old_password, new_hash):
    old_password = old_password.decode('utf-8')
    new_hash = new_hash.decode('utf-8')
    conn = mysql.connector.connect(
        host=config.host,
        user=config.user,
        passwd=config.passwd,
        database=config.database)
    cursor = conn.cursor()
    sql = "UPDATE notes SET password='%s' WHERE password='%s'"
    val = (new_hash, old_password)

    cursor.execute(sql % val)
    conn.commit()
    conn.close()


profile_edit_page = blueprints.Blueprint(
    'profile_edit_page', __name__, static_folder='static', template_folder='templates')

profile_page = blueprints.Blueprint(
    'profile_page', __name__, static_folder='static', template_folder='templates')

verify_page = blueprints.Blueprint(
    'verified', __name__, static_folder='static', template_folder='templates')


@profile_edit_page.route("/profile_edit", methods=['GET', 'POST'])
def profile_edit():

    if request.method == 'POST':
        username = request.form['username']
        old_pwd = request.form["old_pwd"]
        new_pwd = request.form["new_pwd"]

        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            passwd=config.passwd,
            database=config.database)
        cursor = conn.cursor()
        sql = "SELECT username,password FROM notes"

        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        usernames = []
        pwds = []
        userRegex = "^[a-zA-Z0-9_.-]+$"
        for i in range(len(result)):
            usernames.append(result[i][0])
            pwds.append(result[i][1])
        update_username = False
        update_pwd = False
        index = usernames.index(session["username"])
        hashed_pwd = pwds[index]

        pwd = old_pwd.encode('UTF-8')

        new_password = new_pwd.encode('UTF-8')

        hashed_pwd = hashed_pwd.encode("UTF-8")

        if not session["username"] == username:
            if not username:
                return jsonify({"error": "Username is required"})
            elif len(username) > 50:
                return jsonify({"error": "Username too long"})
            elif username in usernames:
                return jsonify({"error": "Username already exists"})
            elif not re.match(userRegex, username):
                return jsonify({"error": "Enter a valid username"})
            else:
                update_username = True
        else:
            pass

        if old_pwd == "" or new_pwd == "":
            pass
        elif len(new_pwd) > 150:
            return jsonify({"error": "Password too long"})
        elif len(new_pwd) < 8:
            return jsonify({"error": "Password too short"})
        elif not bcrypt.checkpw(pwd, hashed_pwd):
            return jsonify({"error": "Password is incorrect"})
        elif bcrypt.checkpw(new_password, hashed_pwd):
            return jsonify({"error": "New Password and old password cannot be the same"})
        else:
            update_pwd = True

        if update_username and update_pwd:
            old_username = session["username"]
            new_username = username
            update_user(old_username, new_username)
            session["username"] = new_username

            old_password = hashed_pwd
            new_hash = bcrypt.hashpw(new_password, bcrypt.gensalt())
            update_password(old_password, new_hash)

            return jsonify({"success": "Updated username and password"})
            # update username and password
        elif update_username:
            old_username = session["username"]
            new_username = username
            update_user(old_username, new_username)
            session["username"] = new_username
            return jsonify({"success": "Updated username"})

        elif update_pwd:
            # update password
            old_password = hashed_pwd
            new_hash = bcrypt.hashpw(new_password, bcrypt.gensalt())
            update_password(old_password, new_hash)
            return jsonify({"success": "Updated password"})
        else:
            return jsonify({"nothing": "ok"})

    return render_template("profile_edit.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"])


@profile_page.route("/profile", methods=['GET', 'POST'])
def profile():
    if request.method == "POST":
        if request.form.get("thumbnail"):
            img_url = request.form["thumbnail"]
            username = request.form["name-url"]

            def is_url_image(image_url):
                try:
                    image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp", "image/tiff",
                                     "image/vnd.microsoft.icon", "image/x-icon", "image/vnd.djvu", "image/svg+xml")
                    r = requests.head(image_url)
                    if r.headers["content-type"] in image_formats:
                        return True
                    return False
                except:
                    return False

            if is_url_image(img_url) and username:

                conn = mysql.connector.connect(
                    host=config.host,
                    user=config.user,
                    passwd=config.passwd,
                    database=config.database)
                cur = conn.cursor()
                session["pfp"] = img_url

                sql = "UPDATE notes SET pfp = '%s' WHERE username= '%s'"
                val = (img_url, username)
                cur.execute(sql % val)
                conn.commit()
                conn.close()

                return render_template("profile.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"])

        elif request.form.get("del-username"):
            username = request.form["del-username"]

            conn = mysql.connector.connect(
                host=config.host,
                user=config.user,
                passwd=config.passwd,
                database=config.database)
            cur = conn.cursor()

            sql = "DELETE FROM notes WHERE username = '%s'"
            val = (username)
            cur.execute(sql % val)
            conn.commit()
            conn.close()

            conn = sqlite.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("PRAGMA key='{}'".format(config.db_pwd))
            cur.execute("DELETE FROM editor WHERE email = :email",
                        {"email": session["email"]})
            conn.commit()
            conn.close()

            return redirect('/logout')

        elif 'file' in request.files:
            def allowed_file(filename): return '.' in filename and filename.rsplit(
                '.', 1)[1].lower() in ALLOWED_EXTENSIONS

            file = request.files['file']
            username = request.form["name-upload"]
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)
                file.save(os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename))

                filename = "static/imgs/" + filename
                conn = mysql.connector.connect(
                    host=config.host,
                    user=config.user,
                    passwd=config.passwd,
                    database=config.database)
                cur = conn.cursor()

                session["pfp"] = filename

                sql = "UPDATE notes SET pfp = '%s' WHERE username= '%s'"
                val = (filename, username)
                cur.execute(sql % val)
                conn.commit()
                conn.close()

                return render_template("profile.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"])

    return render_template("profile.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"])


@verify_page.route("/verify", methods=['GET', 'POST'])
def verify():
    if session["verified"]:
        return redirect(url_for("index.index"))
    else:
        if request.method == "POST":
            if request.form.get("email"):
                email = request.form["email"]
                try:
                    code = Email_To(session["email"])
                    session["code"] = code
                    return jsonify({"success": True})
                except:
                    return jsonify({"error": True})
            if request.form.get("code"):
                code = request.form["code"]
                if int(code) == int(session["code"]):
                    conn = mysql.connector.connect(
                        host=config.host,
                        user=config.user,
                        passwd=config.passwd,
                        database=config.database)
                    cursor = conn.cursor()
                    sql = "UPDATE notes SET email_confirmation='%s' WHERE email='%s'"
                    val = ('True', session["email"])

                    cursor.execute(sql % val)

                    conn.commit()
                    conn.close()
                    session["verified"] = True
                    return jsonify({"success": True})
                else:
                    return jsonify({"success": False})

        return render_template("verify.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"])

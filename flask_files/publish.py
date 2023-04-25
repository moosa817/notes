from flask import session, request, blueprints, redirect, url_for, render_template, jsonify
import config
import mysql.connector
from pymongo import MongoClient


client = MongoClient(config.mongo_str)
db = client.get_database('notes')
records = db.notes_data


publish_page = blueprints.Blueprint(
    'publish', __name__, static_folder='static', template_folder='templates')


def EmailToUsername(email_list):
    conn = mysql.connector.connect(
        host=config.host,
        user=config.user,
        passwd=config.passwd,
        database=config.database)
    cursor = conn.cursor()

    format_strings = ','.join(['%s'] * len(email_list))
    cursor.execute("SELECT username FROM notes WHERE email IN (%s)" % format_strings,
                   tuple(email_list))

    results = cursor.fetchall()
    conn.close()
    users = []
    for i in results:
        users.append(i[0])

    return users


@publish_page.route("/publish", methods=["GET", "POST"])
def publish():
    if session.get("username"):
        if request.method == "POST":
            if request.form.get("to_publish"):
                to_publish = request.form.get("to_publish")
                try:
                    records.update_one({"email": session["email"], "filename": to_publish}, {
                                       "$set": {"published": True}})
                    return jsonify({"success": True})
                except Exception as E:
                    return jsonify({"success": False})

    # un_publish
            if request.form.get("un_publish"):
                un_publish = request.form.get("un_publish")
                try:
                    records.update_one({"email": session["email"], "filename": un_publish}, {
                                       "$set": {"published": False}})

                    return jsonify({"success": True})
                except Exception as E:
                    return jsonify({"success": False})

        verified = []
        not_verified = []

        for i in records.find({"email": session["email"], "published": True}):
            verified.append(i["filename"])

        for i in records.find({"email": session["email"], "published": False}):
            not_verified.append(i["filename"])

        published = verified
        not_published = not_verified

        return render_template("publish.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], published=published, not_published=not_published)
    else:
        return render_template("index.html")


@publish_page.route("/public", methods=["GET"])
def public():
    file_name = request.args.get("name")
    u = request.args.get("username")
    if file_name and u:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            passwd=config.passwd,
            database=config.database)
        cursor = conn.cursor()
        sql = "SELECT email FROM notes WHERE username = %s"
        val = (u,)
        cursor.execute(sql, val)
        email = cursor.fetchone()
        conn.close()

        if email:
            email = email[0]
            result = records.find_one(
                {"email": email, "published": True, "filename": file_name})

            if result:
                filename = result["filename"]
                editor_data = result["editor_data"]

                if session.get("username"):
                    return render_template("public.html", user=u, filename=filename, editor_data=editor_data, username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], show=True)
                else:
                    return render_template("public.html", user=u, filename=filename, editor_data=editor_data, show=True)
            else:
                return redirect("/public")

        return redirect("/public")

    # normally return public.html
    result = records.find({"published": True})

    emails = []
    filenames = []
    editor_data = []

    for i in result:
        emails.append(i["email"])
        filenames.append(i["filename"])
        editor_data.append(i["editor_data"])

    users = EmailToUsername(emails)

    if session.get("username"):

        return render_template("public.html", user=users, files=filenames, editor_data=editor_data, username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"])
    else:
        return render_template("public.html", user=users, files=filenames, editor_data=editor_data)

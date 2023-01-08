from flask import session, request, blueprints, jsonify, render_template, redirect
from pysqlcipher3 import dbapi2 as sqlite
import config

notes_page = blueprints.Blueprint(
    'notes', __name__, static_folder='static', template_folder='templates')


@notes_page.route("/notes", methods=["GET", "POST"])
def notes():
    if session.get("username"):
        if request.method == "POST":

            editor_data = request.form["editor_data"]

            name = request.form["name"]

            conn = sqlite.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("PRAGMA key='{}'".format(config.db_pwd))

            cur.execute("UPDATE editor SET editor_data=:editor_data WHERE filename = :name AND email=:email", {
                        "editor_data": editor_data, "name": name, "email": session["email"]})

            conn.commit()
            conn.close()
            return jsonify({"success": True})

        if request.args.get("name"):
            if session.get("username"):
                name = request.args.get("name")
                conn = sqlite.connect("notes_data.db")
                cur = conn.cursor()
                cur.execute("PRAGMA key='{}'".format(config.db_pwd))

                cur.execute("SELECT editor_data FROM editor WHERE filename = :orignal_input AND email = :email", {
                            "orignal_input": name, "email": session["email"]})

                results = cur.fetchall()
                result = results[0][0]
                if result == None:
                    result = ""

                return render_template("notes.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], stuff=result, file_name=name)

        else:
            return redirect("/")
    else:
        return render_template("index.html")

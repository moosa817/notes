from flask import session, request, blueprints, jsonify, render_template, redirect
import config
from pymongo import MongoClient



client = MongoClient(config.mongo_str)
db = client.get_database('notes')
records = db.notes_data


notes_page = blueprints.Blueprint(
    'notes', __name__, static_folder='static', template_folder='templates')


@notes_page.route("/notes", methods=["GET", "POST"])
def notes():
    if session.get("username"):
        if request.method == "POST":

            editor_data = request.form["editor_data"]

            name = request.form["name"]

            records.update_one({"email":session["email"],"filename":name},{"$set":{"editor_data":editor_data}})
            
            def utf8len(s):return ((len(s.encode('utf-8')))/1024)/1024

            size = utf8len(editor_data)
            size = round(size,4)
            
            return jsonify({"success": True,"size":size})

        if request.args.get("name"):
            if session.get("username"):
                name = request.args.get("name")

                result = records.find_one({"email":session["email"],"filename":name})
                result = result["editor_data"]

                def utf8len(s):return ((len(s.encode('utf-8')))/1024)/1024

                size = utf8len(result)
                size = round(size,4)
                return render_template("notes.html", username=session["username"], email=session["email"], verified=session["verified"], pfp=session["pfp"], files=session["files"], stuff=result, file_name=name,size=size)

        else:
            return redirect("/")
    else:
        return render_template("index.html")

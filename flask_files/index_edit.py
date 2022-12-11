from flask import session,request,blueprints,jsonify,render_template
import re
from pysqlcipher3 import dbapi2 as sqlite
import config


index_edit_page = blueprints.Blueprint('index_edit_page', __name__,static_folder='static',template_folder='templates')

view_page = blueprints.Blueprint('view_edit_page', __name__,static_folder='static',template_folder='templates')

download_name_page = blueprints.Blueprint('download_name_page', __name__,static_folder='static',template_folder='templates')


delete_name_page = blueprints.Blueprint('delete_name_page ', __name__,static_folder='static',template_folder='templates')

@index_edit_page.route("/edit_name",methods=["POST","GET"])
def edit_name():
    if request.method == "POST":
        file_regex = "^[ a-zA-Z0-9_.-]+$"
        input1 = request.form["input1"]
        input2 = request.form["input2"]
        if len(input1) == 0:
            return jsonify({"error":"Please Enter a name."})
        elif len(input1) > 50:
            return jsonify({'errror':"Rename failed , name too long"})
        elif not re.match(file_regex, input1):
            print(input1)
            return jsonify({"error": "Enter a valid name."})
        else:
            new_input = input1
            original_input = input2
            index = session["files"].index(original_input)
            session["files"][index] = new_input
            # add new input to database replacing it with original input
            conn = sqlite.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("PRAGMA key='{}'".format(config.db_pwd))
            cur.execute("UPDATE editor SET filename = :new_input WHERE filename= :orignal_input",{"new_input":new_input, "orignal_input":original_input})

            conn.commit()
            conn.close()
            return jsonify({"success":"renamed successfully"})

@delete_name_page.route("/delete_name",methods=["POST"])
def delete_name():
    if request.method == "POST":
        delete_input = request.form["delete_input"]
        try:
            session["files"].remove(delete_input)
            conn = sqlite.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("PRAGMA key='{}'".format(config.db_pwd))
            cur.execute("DELETE FROM editor WHERE filename = :orignal_input", {"orignal_input":delete_input})
            conn.commit()
            conn.close()
            return jsonify({"success":True})
        except:
            return jsonify({"success": False})
        
@download_name_page.route("/download_name",methods=["GET", "POST"])
def download_name():
    if request.method == "POST":
        download_file = request.form["download_file"]
        
        conn = sqlite.connect("notes_data.db")
        cur  = conn.cursor()
        cur.execute("PRAGMA key='{}'".format(config.db_pwd))
        cur.execute("SELECT editor_data FROM editor WHERE filename = :orignal_input", {"orignal_input":download_file})

        results = cur.fetchall()
        result = results[0][0]
        if result == None:
            result = ""
        return jsonify({"success":True,"data":result})

@view_page.route("/view/<n>")
def view_name(n):
    n = int(n)
    n = n-1
    name = session["files"][n]
    conn = sqlite.connect("notes_data.db")
    cur  = conn.cursor()
    cur.execute("PRAGMA key='{}'".format(config.db_pwd))
    cur.execute("SELECT editor_data FROM editor WHERE filename = :orignal_input", {"orignal_input":name})

    results = cur.fetchall()
    result = results[0][0]
    if result == None:
        result = ""

    return render_template("view.html",stuff=result,file_name=name)


from flask import session,request,blueprints,redirect,url_for,render_template
import re
from pysqlcipher3 import dbapi2 as sqlite
import config


index_page = blueprints.Blueprint('index', __name__,static_folder='static',template_folder='templates')



@index_page.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        filename = request.form['filename']
        file_regex = "^[ a-zA-Z0-9_.-]+$"
        if re.match(file_regex, filename) and len(filename) > 0 and len(filename) < 50:
            conn = sqlite.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("PRAGMA key='{}'".format(config.db_pwd))
            email = session["email"]

            res = cur.execute("SELECT * FROM editor WHERE email=:email AND filename=:filename", {"email":email, "filename":filename})

            if not res.fetchall():
                cur.execute("INSERT INTO editor (email, filename) VALUES (:email, :filename)", {"email":email, "filename":filename})
                conn.commit()
                conn.close()
                session["files"].append(filename)

                return render_template("index.html",username= session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],success="File Created",files=session["files"])
            else:
                return render_template("index.html",username= session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],error="File Already Exists",files=session["files"])
        else:
            return render_template("index.html",username= session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],error="Enter a valid filename",files=session["files"])
        
    if session.get("username"):
        email = session["email"]
        conn = sqlite.connect("notes_data.db")
        cur = conn.cursor()
        cur.execute("PRAGMA key='{}'".format(config.db_pwd))
        result = cur.execute("SELECT * FROM editor WHERE email=:email", {"email":email})

        result = result.fetchall()
        # print(result)

        files = []
        for i in result:
            files.append(i[2])

        session["files"] = files

        return render_template("index.html",username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],files=session["files"])
    else:
        return render_template("index.html")
        
@index_page.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index.index"))


@index_page.route("/test",methods=["GET", "POST"])
def test():
    return 'sent'
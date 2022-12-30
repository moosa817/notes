from flask import session,request,blueprints,redirect,url_for,render_template,jsonify
import re
from pysqlcipher3 import dbapi2 as sqlite
import config
import mysql.connector

publish_page = blueprints.Blueprint('publish', __name__,static_folder='static',template_folder='templates')


@publish_page.route("/publish",methods=["GET","POST"])
def publish():
    if session.get("username"):
        if request.method == "POST":
            if request.form.get("to_publish"):
                to_publish = request.form.get("to_publish")
                try:
                    conn = sqlite.connect("notes_data.db")
                    cur = conn.cursor()
                    cur.execute("PRAGMA key='{}'".format(config.db_pwd))
                    cur.execute("UPDATE editor SET published=:published WHERE email = :email AND filename=:filename", {"published":'True',"email":session["email"],"filename":to_publish})
                    conn.commit()
                    conn.close()


                    return jsonify({"success":True})
                except Exception as E:
                    print(E)
                    return jsonify({"success": False})
                
    # un_publish
            if request.form.get("un_publish"):
                to_publish = request.form.get("un_publish")
                try:
                    conn = sqlite.connect("notes_data.db")
                    cur = conn.cursor()
                    cur.execute("PRAGMA key='{}'".format(config.db_pwd))
                    cur.execute("UPDATE editor SET published=:published WHERE email = :email AND filename=:filename", {"published":None,"email":session["email"],"filename":to_publish})
                    conn.commit()
                    conn.close()


                    return jsonify({"success":True})
                except Exception as E:
                    print(E)

                    return jsonify({"success": False})
            



        conn = sqlite.connect("notes_data.db")
        cur = conn.cursor()
        cur.execute("PRAGMA key='{}'".format(config.db_pwd))
        cur.execute("SELECT * FROM editor WHERE email=:email", {"email":session["email"]})
        


        not_verified = []
        verified = []


        result = cur.fetchall()
        for i in result:
            if not i[3]:
                not_verified.append(i[2])
            else:
                verified.append(i[2])

        published = verified
        not_published = not_verified

        return render_template("publish.html",username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],files=session["files"],published=published,not_published=not_published)
    else:
        return render_template("index.html")


@publish_page.route("/public",methods=["GET"])
def public():
    g = request.args.get("name")
    u = request.args.get("username")
    if g and u:
        conn = mysql.connector.connect(
        host=config.host,
        user=config.user,
        passwd=config.passwd,
        database=config.database)
        cursor = conn.cursor()
        sql = "SELECT email FROM notes WHERE username = %s"
        val = (u,)
        cursor.execute(sql,val)
        email = cursor.fetchone()
        conn.close()

        if email:
            email = email[0]
            conn = sqlite.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("PRAGMA key='{}'".format(config.db_pwd))
            cur.execute("SELECT filename,editor_data FROM editor WHERE published='True' AND filename = :filename AND email = :email",{"filename":g,"email":email})



            result = cur.fetchall()
            conn.close()
            if result:
                filename = result[0][0]
                editor_data = result[0][1]
                if editor_data == None:
                    editor_data = ""
                # print(filename,editor_data)
                if session.get("username"):
                    return render_template("public.html",user=u,filename=filename,editor_data=editor_data,username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],files=session["files"],show=True)
                else:
                    return render_template("public.html",user=u,filename=filename,editor_data=editor_data,show=True)
            else:
                return redirect("/public")


          
        return redirect("/public")




    #normally return public.html
    return render_template("public.html")

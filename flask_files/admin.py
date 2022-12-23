from flask import session,request,blueprints,redirect,url_for,render_template
import re
from pysqlcipher3 import dbapi2 as sqlite
import config


admin_page = blueprints.Blueprint('admin_page', __name__,static_folder='static',template_folder='templates')


@admin_page.route("/admin",methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form.get("pwd"):
            pwd = request.form["pwd"]
            if pwd == config.db_pwd:
                session["admin"] = True
                return redirect("/admin")
            else:
                return render_template("admin.html",login=False,error="wrong pwd")
    
        if request.form.get("input1"):
            input1 = request.form["input1"]
            email = request.form["email"]
            

            conn = sqlite.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("PRAGMA key='{}'".format(config.db_pwd))
            cur.execute("UPDATE use_media SET status = :status WHERE email = :email",{"status":input1,"email":email})
            conn.commit()
            conn.close()
            

            
        
    if session.get("admin"):
        page = request.args.get("page")
        if page == "editor":
            conn = sqlite.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("PRAGMA key='{}'".format(config.db_pwd))
            cur.execute("SELECT * FROM editor")
            result = cur.fetchall()
            conn.commit()
            conn.close()
            
            email = []
            filename = []
            editor_data = []
            id = 0
            ids = []
            for i in result:
                id = id+1
                ids.append(id) 
                email.append(i[1])
                filename.append(i[2])
                editor_data.append(i[3])

        
            return render_template("admin.html",login=True,ids=ids,email=email,filename=filename,editor_data=editor_data,page1=True)

        elif page == "verify":
            conn = sqlite.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("PRAGMA key='{}'".format(config.db_pwd))
            cur.execute("SELECT * FROM use_media")
            result = cur.fetchall()
            conn.commit()
            conn.close()
            
            email = []
            use_email = []
            status = []
            id = 0
            ids = []
            for i in result:
                id = id+1
                ids.append(id) 
                email.append(i[1])
                use_email.append(i[2])
                status.append(i[3])

            




            return render_template("admin.html",login=True,ids=ids,email=email,use_email=use_email,status=status,page2=True)

        elif page == "logs":
            return render_template("admin.html",login=True)
        else:
            return render_template("admin.html",login=True)

    


    print("here")
    return render_template("admin.html",login=False)

    
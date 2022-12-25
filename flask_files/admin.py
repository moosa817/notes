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
    
        if request.form.get("delete_email"):
            to_delete = request.form.get("delete_email")
            conn = sqlite.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("PRAGMA key='{}'".format(config.db_pwd))
            cur.execute("DELETE FROM use_media WHERE email = :email",{"email":to_delete})
            conn.commit()
            conn.close()

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
        if request.form.get("email1") and request.form.get("email_to_use1") and request.form.get("status1"):
            email = request.form["email1"]
            email_to_use = request.form["email_to_use1"]
            status = request.form["status1"]

            emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if not re.match(emailRegex,email) or not re.match(emailRegex,email_to_use):
                pass
            else:
                conn = sqlite.connect("notes_data.db")
                cur = conn.cursor()
                cur.execute("PRAGMA key='{}'".format(config.db_pwd))
                cur.execute("INSERT INTO use_media (email,email_to_use,status) VALUES (:1,:2,:3)" , {'1':email,'2':email_to_use,'3':status}) 
                conn.commit()
        








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

    
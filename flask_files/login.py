import mysql.connector
from flask import session,request,blueprints,redirect,url_for,render_template
import config
import bcrypt

login_page = blueprints.Blueprint('login', __name__,static_folder='static',template_folder='templates')


@login_page.route("/login",methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("index.index"))
    else:
        if request.method == 'POST':
            umail = request.form['umail']
            pwd = request.form['pwd']
            conn = mysql.connector.connect(
                host=config.host,
                user=config.user,
                passwd=config.passwd,
                database=config.database)
            cursor = conn.cursor()
            sql = "SELECT username,email,password,pfp,email_confirmation FROM notes"
            
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.commit()
            conn.close()
         
            emails = []
            users = []
            pwds = []
            email_verifications = []
            pfps = []
            for i in range(len(result)):
                users.append(result[i][0])
                emails.append(result[i][1])
                pwds.append(result[i][2])
                pfps.append(result[i][3])
                email_verifications.append(result[i][4])

            if umail in emails:
                form1 = umail
            elif umail in users:
                form1 = umail
            else:
                return render_template("login.html",error="Username or Email doesn't exist",umail=umail,pwd=pwd)


            try:
                index = emails.index(form1)
            except:
                index = users.index(form1)


            hashed_pwd = pwds[index]
            pwd = pwd.encode('UTF-8')
            hashed_pwd  = hashed_pwd.encode("UTF-8")
            if bcrypt.checkpw(pwd, hashed_pwd):
                session["username"] = users[index]
                session["email"] = emails[index]
                session["verified"] = email_verifications[index]
                session["pfp"] = pfps[index]
                return redirect(url_for("index.index"))
            else:
                return render_template("login.html",error="Wrong password",umail=umail)



        return render_template("login.html")
